from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    user_id: int
    content: str


class PostRead(BaseModel):
    id: int
    user_id: int
    content: str


class PostUpdate(BaseModel):
    content: str | None = None
