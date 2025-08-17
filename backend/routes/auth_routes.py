from fastapi import APIRouter, Request, status
from services.jwt_service import generate_token, validate_token
from utils.logger import logger

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    token = generate_token(username)
    return {"token": token}

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