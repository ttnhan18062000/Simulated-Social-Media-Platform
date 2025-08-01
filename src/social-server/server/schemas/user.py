from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel
from pydantic import ConfigDict
from server.schemas.post import PostRead


class UserBase(SQLModel):
    username: str
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str  # Plain password from client


class UserUpdate(SQLModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    last_active_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserReadWithPosts(UserRead):
    posts: List[PostRead] = []

    model_config = ConfigDict(from_attributes=True)
