from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


# ------------------------------
# Base Schema
# ------------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


# ------------------------------
# Schema for registration
# ------------------------------
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "USER"

    @validator("role")
    def normalize_role(cls, value):
        # Convert role to uppercase to match SQLAlchemy Enum
        return value.lower()


# ------------------------------
# Schema for login
# ------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ------------------------------
# Schema for returning user data
# ------------------------------
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM model → Pydantic conversion


# ------------------------------
# Token schema
# ------------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
