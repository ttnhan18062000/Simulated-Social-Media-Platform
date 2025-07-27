from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import ConfigDict


class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str  # only needed on creation


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
