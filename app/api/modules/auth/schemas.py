from __future__ import annotations
from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic.types import constr

class UserBase(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=50) = Field(
        ..., description= "Unique username between 3 and 50 characters"
    )
    email: EmailStr = Field(..., description= "Valid email address")
    full_name: Optional[str] = Field(None, description= "Full name of the user")

    @field_validator("email")
    @classmethod
    def normalize_email (cls, v: EmailStr) -> EmailStr:
        return Email(v.lower())



class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128) = Field(
        ..., description="Password must be 8-128 characters, with mixed complexity"
    )

    @staticmethod
    def validate_password_strength(password: str):
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*]", password):
            raise ValueError("Password must contain at least one special character.")

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()

    @staticmethod
    def password_validator(v):
        UserCreate.validate_password_strength(v)
        return v
        
class UserLogin(BaseModel):
    username: Optional[str] = Field(None, description= "Username for login")
    email: EmailStr = Field(..., description= "Email for login")
    password: constr(min_length=8, max_length=128)

    @root_validator(pre=True)
    def at_least_one_field(cls, values):
        username, email = values.get("username"), values.get("email")

class UserResponse(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


