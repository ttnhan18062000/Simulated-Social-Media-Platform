from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
