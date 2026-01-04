from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    nama_user: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id_user: int

    class Config:
        from_attributes = True