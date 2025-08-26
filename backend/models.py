from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from db import Base

class FileMetadata(Base):
    __tablename__ = 'file_metadata'
    file_id = Column(String, primary_key=True, index=True)
    orig_name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=True)
    secret_hash = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    secret_attempts = Column(Integer, default=0, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reset_token = Column(String, nullable=True, index=True)
    reset_expires_at = Column(DateTime(timezone=True), nullable=True)
