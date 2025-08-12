from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String (50), unique=True, index=True, nullable=False)
    email = Column(String (120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(50), default="user", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)