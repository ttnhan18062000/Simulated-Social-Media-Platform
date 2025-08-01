from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserFeedCreate(BaseModel):
    user_id: int
    post_id: int
    rank_score: Optional[float] = None
    source_type: Optional[str] = "follow"
    visibility: Optional[str] = "public"


class UserFeedRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    added_at: datetime
    rank_score: Optional[float]
    source_type: str
    is_seen: bool
    visibility: str

    class Config:
        from_attributes = True


class UserFeedUpdate(BaseModel):
    is_seen: Optional[bool] = None
    rank_score: Optional[float] = None
