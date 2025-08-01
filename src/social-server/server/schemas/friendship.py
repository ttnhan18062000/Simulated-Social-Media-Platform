from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FriendshipCreate(BaseModel):
    user_id: int
    friend_id: int
    status: str  # "requested", "accepted", "blocked"


class FriendshipRead(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FriendshipUpdate(BaseModel):
    status: Optional[str] = None  # Allow status updates only
