from fastapi import FastAPI
import asyncio
from db import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routes.upload_routes import router as upload_router
from routes.auth_routes import router as auth_router
from routes.health_routes import router as health_router

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api/uploads", tags=["uploads"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(health_router, prefix="/api/health", tags=["health"])

@app.get("/")
def read_root():
    return {"message": "Welcome to VaultUpload API!"}

@app.on_event("startup")
async def on_startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)