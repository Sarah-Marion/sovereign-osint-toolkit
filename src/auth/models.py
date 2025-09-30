from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class User(UserBase):
    id: str
    disabled: bool = False
    roles: List[str] = []
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = []

class LoginRequest(BaseModel):
    username: str
    password: str

class Role(BaseModel):
    name: str
    permissions: List[str]
    description: str