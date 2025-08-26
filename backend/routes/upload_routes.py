
from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from google.cloud import storage
from utils.logger import logger
from utils.security_utils import hash_password, verify_password
from services.jwt_service import generate_share_token, decode_share_token
from urllib.parse import urlencode
from services.scan_service import scan_file
from datetime import datetime, timedelta, timezone
import os
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import FileMetadata
import uuid

router = APIRouter()

MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB
GCS_BUCKET_NAME = "vaultupload2025_1"  # TODO: Replace with your actual bucket name

def get_gcs_client():
    return storage.Client()

MAX_SECRET_ATTEMPTS = 2

def _ensure_aware(dt: datetime) -> datetime:
    """Convert naive datetime (assumed UTC) to timezone-aware UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

IST_OFFSET = timezone(timedelta(hours=5, minutes=30))

def _format_ist(dt: datetime) -> str:
    try:
        aware = _ensure_aware(dt)  # treat naive as UTC
        return aware.astimezone(IST_OFFSET).strftime('%d-%m-%Y %H:%M:%S IST')
    except Exception:
        try:
            return dt.isoformat()
        except Exception:
            return str(dt)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    expiry_hours: int = 24,
    secret_word: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    request: Request = None,
):
    """Upload a file, optional secret, set expiry, virus scan, store metadata."""
    if expiry_hours < 1 or expiry_hours > 24:
        raise HTTPException(status_code=400, detail="expiry_hours must be between 1 and 24")
    try:
        # Read & size-check
        size = 0
        chunks: List[bytes] = []
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                logger.warning(f"Upload rejected (too large): {file.filename} size={size}")
                raise HTTPException(status_code=413, detail="File too large (max 250MB)")
            chunks.append(chunk)
        data = b"".join(chunks)

        # Scan
        scan_result = scan_file(file.filename, data)
        if not scan_result.get("is_clean", False):
            raise HTTPException(status_code=400, detail=f"Virus scan failed: {scan_result.get('reason','unknown')}")

        # Store in GCS
        client = get_gcs_client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        file_id = f"{uuid.uuid4()}_{file.filename}"
        blob = bucket.blob(file_id)
        blob.upload_from_string(data, content_type=file.content_type or "application/octet-stream")

        # DB metadata
        expires_at = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=expiry_hours)
        db_obj = FileMetadata(
            file_id=file_id,
            orig_name=file.filename,
            size=size,
            content_type=file.content_type or "application/octet-stream",
            secret_hash=hash_password(secret_word) if secret_word else None,
            expires_at=expires_at,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        logger.info(f"Uploaded file {file_id} metadata stored (db)")

        # Response assembly
        expires_ist_str = _format_ist(db_obj.expires_at)
        frontend_base = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
        share_token = generate_share_token(file_id, db_obj.expires_at)
        query = urlencode({"fileId": file_id, "token": share_token})
        receive_link = f"{frontend_base.rstrip('/')}/receive?{query}"
        logger.info(f"Generated receive_link {receive_link} for file {file_id}")
        return {
            "message": "File uploaded",
            "file_id": file_id,
            "metadata": {
                "file_id": db_obj.file_id,
                "orig_name": db_obj.orig_name,
                "size": db_obj.size,
                "expires_at": db_obj.expires_at.isoformat(),
                "expires_at_ist": expires_ist_str,
                "secret_hash": db_obj.secret_hash,
                "requires_secret": bool(db_obj.secret_hash),
                "created_at": db_obj.created_at.isoformat() if db_obj.created_at else None,
                "receive_link": receive_link,
                "share_token": share_token,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("")
async def list_files(session: AsyncSession = Depends(get_session)):
    try:
        now = datetime.now(timezone.utc)
        stmt = select(FileMetadata).where(FileMetadata.deleted == False, FileMetadata.expires_at > now)  # noqa
        result = await session.execute(stmt)
        files = result.scalars().all()
        rows = []
        for f in files:
            rows.append({
                "name": f.orig_name,
                "file_id": f.file_id,
                "size": f.size,
                "expires_at": f.expires_at.isoformat(),  # UTC ISO
                "expires_at_ist": _format_ist(f.expires_at),
                "downloadUrl": f"/api/uploads/download/{f.file_id}",
                "requires_secret": bool(f.secret_hash),
                "orig_name": f.orig_name
            })
        return {"files": rows}
    except Exception as e:
        logger.exception("List files failed")
        raise HTTPException(status_code=500, detail=f"List failed: {str(e)}")

@router.get("/share/{file_id}")
async def generate_share(file_id: str, session: AsyncSession = Depends(get_session)):
    stmt = select(FileMetadata).where(FileMetadata.file_id == file_id, FileMetadata.deleted == False)  # noqa
    result = await session.execute(stmt)
    meta = result.scalar_one_or_none()
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")
    exp = _ensure_aware(meta.expires_at)
    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="File expired")
    share_token = generate_share_token(file_id, exp)
    return {"share_token": share_token, "expires_at": exp.isoformat(), "expires_at_ist": _format_ist(exp), "requires_secret": bool(meta.secret_hash)}

@router.post("/access/{file_id}")
async def access_file(file_id: str, token: str = Body(...), secret_word: Optional[str] = Body(default=None), session: AsyncSession = Depends(get_session)):
    stmt = select(FileMetadata).where(FileMetadata.file_id == file_id, FileMetadata.deleted == False)  # noqa
    result = await session.execute(stmt)
    meta = result.scalar_one_or_none()
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")
    exp = _ensure_aware(meta.expires_at)
    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="File expired")
    try:
        payload = decode_share_token(token)
        if payload.get("sid") != file_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    if meta.secret_hash:
        # Provide clearer feedback before counting attempts
        if not secret_word:
            raise HTTPException(status_code=400, detail="Secret required")
        if meta.secret_attempts >= MAX_SECRET_ATTEMPTS:
            raise HTTPException(status_code=429, detail="Too many attempts")
        if not verify_password(meta.secret_hash, secret_word):
            await session.execute(update(FileMetadata).where(FileMetadata.file_id == file_id).values(secret_attempts=FileMetadata.secret_attempts + 1))  # type: ignore
            await session.commit()
            raise HTTPException(status_code=401, detail="Invalid secret")
        # reset attempts on success
        await session.execute(update(FileMetadata).where(FileMetadata.file_id == file_id).values(secret_attempts=0))
        await session.commit()
    client = get_gcs_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file_id)
    if not blob.exists():
        raise HTTPException(status_code=404, detail="File not found")
    stream = blob.open("rb")
    return StreamingResponse(stream, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={meta.orig_name}"})

@router.get("/download/{file_id}")
async def download(file_id: str):
    # Simple direct download without share security (could be restricted later)
    client = get_gcs_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file_id)
    if not blob.exists():
        raise HTTPException(status_code=404, detail="File not found")
    stream = blob.open("rb")
    return StreamingResponse(stream, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_id}"})

@router.delete("/{file_id}")
async def delete_file(file_id: str, session: AsyncSession = Depends(get_session)):
    try:
        stmt = select(FileMetadata).where(FileMetadata.file_id == file_id, FileMetadata.deleted == False)  # noqa
        result = await session.execute(stmt)
        meta = result.scalar_one_or_none()
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        client = get_gcs_client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(file_id)
        if blob.exists():
            blob.delete()
        await session.execute(update(FileMetadata).where(FileMetadata.file_id == file_id).values(deleted=True))
        await session.commit()
        logger.info(f"Deleted file {file_id}")
        return {"message": "Deleted", "filename": file_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Delete failed")
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
