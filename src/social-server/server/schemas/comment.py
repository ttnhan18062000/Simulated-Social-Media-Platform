from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content_text: str


class CommentRead(BaseModel):
    id: int
    post_id: int
    user_id: int
    content_text: str
    created_at: datetime

    class Config:
        from_attributes = True
