from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReactionCreate(BaseModel):
    post_id: int
    user_id: int
    type: str  # like, upvote, etc.


class ReactionRead(BaseModel):
    id: int
    post_id: int
    user_id: int
    type: str
    created_at: datetime

    class Config:
        from_attributes = True
