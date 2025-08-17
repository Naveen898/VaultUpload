from fastapi import APIRouter, UploadFile, File, HTTPException
from services.storage_service import upload_file, download_file
from services.scan_service import scan_file
from utils.file_utils import validate_file
from utils.logger import logger

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type")
    scan_result = scan_file(file)
    if not scan_result['is_clean']:
        raise HTTPException(status_code=400, detail="File is infected with a virus")
    file_url = upload_file(file)
    return {"url": file_url}

@router.get("/download/{file_id}")
async def download(file_id: str):
    file_data = download_file(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    return file_data