from fastapi import APIRouter, Request, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from db import get_session
from models import User
from utils.security_utils import hash_password, verify_password
from datetime import datetime, timedelta, timezone
import uuid
import os
import httpx
from services.jwt_service import generate_token, validate_token
from services.email_service import send_reset_email
from utils.logger import logger

router = APIRouter()

@router.post("/register")
async def register(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    hcaptcha_token = data.get('hcaptcha_token')
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    # captcha check
    if os.getenv('HCAPTCHA_ENABLED', '0') == '1':
        secret = os.getenv('HCAPTCHA_SECRET')
        if not secret:
            raise HTTPException(status_code=500, detail="Captcha secret not configured")
        if not hcaptcha_token:
            raise HTTPException(status_code=400, detail="Captcha required")
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post('https://hcaptcha.com/siteverify', data={'secret': secret, 'response': hcaptcha_token})
        if resp.status_code != 200 or not resp.json().get('success'):
            raise HTTPException(status_code=400, detail="Captcha failed")
    # uniqueness
    existing = await session.execute(select(User).where(User.username == username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Username taken")
    user = User(username=username, password_hash=hash_password(password), email=email)
    session.add(user)
    await session.commit()
    return {"message": "Registered"}

@router.post("/login")
async def login(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    hcaptcha_token = data.get('hcaptcha_token')
    if os.getenv('HCAPTCHA_ENABLED', '0') == '1':
        secret = os.getenv('HCAPTCHA_SECRET')
        if not secret:
            raise HTTPException(status_code=500, detail="Captcha secret not configured")
        if not hcaptcha_token:
            raise HTTPException(status_code=400, detail="Captcha required")
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post('https://hcaptcha.com/siteverify', data={'secret': secret, 'response': hcaptcha_token})
        if resp.status_code != 200 or not resp.json().get('success'):
            raise HTTPException(status_code=400, detail="Captcha failed")
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(user.password_hash, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = generate_token(username)
    return {"token": token}

@router.post("/forgot")
async def forgot(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()
    username = data.get('username')
    if not username:
        raise HTTPException(status_code=400, detail="Username required")
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        # Avoid user enumeration
        return {"message": "If account exists, reset token issued"}
    token = str(uuid.uuid4())
    expires = datetime.now(timezone.utc) + timedelta(minutes=20)
    await session.execute(update(User).where(User.id == user.id).values(reset_token=token, reset_expires_at=expires))
    await session.commit()
    # Attempt to send email if user has an email set
    if user.email:
        send_reset_email(user.email, user.username, token)
    return {"message": "Reset token generated"}

@router.post("/reset")
async def reset(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()
    token = data.get('token')
    new_password = data.get('new_password')
    if not token or not new_password:
        raise HTTPException(status_code=400, detail="Token and new_password required")
    result = await session.execute(select(User).where(User.reset_token == token))
    user = result.scalar_one_or_none()
    if not user or not user.reset_expires_at or user.reset_expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    await session.execute(update(User).where(User.id == user.id).values(password_hash=hash_password(new_password), reset_token=None, reset_expires_at=None))
    await session.commit()
    return {"message": "Password reset"}

@router.post("/validate")
async def validate(request: Request):
    data = await request.json()
    token = data.get('token')
    if validate_token(token):
        return {"message": "Token is valid"}
    else:
        return {"message": "Token is invalid"}, status.HTTP_401_UNAUTHORIZED

@router.post("/refresh")
async def refresh(request: Request):
    data = await request.json()
    token = data.get('token')
    if validate_token(token):
        new_token = generate_token(data.get('username'))
        return {"token": new_token}
    else:
        return {"message": "Token is invalid"}, status.HTTP_401_UNAUTHORIZED