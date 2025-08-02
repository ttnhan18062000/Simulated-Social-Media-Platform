from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    user_id: int
    content_text: str
    image_url: Optional[str] = None
    visibility: Optional[str] = "public"


class PostRead(BaseModel):
    id: int
    user_id: int
    content_text: str
    image_url: Optional[str]
    visibility: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    content_text: Optional[str] = None
    image_url: Optional[str] = None
    visibility: Optional[str] = None
