from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

# ----------------------------------------
# User
# ----------------------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active_at: Optional[datetime] = None

    posts: List["Post"] = Relationship(back_populates="author")


# ----------------------------------------
# Post
# ----------------------------------------
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content_text: str
    image_url: Optional[str] = None
    visibility: str = Field(default="public")  # public, friends-only, private
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    author: Optional[User] = Relationship(back_populates="posts")


# ----------------------------------------
# Feed
# ----------------------------------------
class Feed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content_text: str
    image_url: Optional[str] = None
    visibility: str = Field(default="public")  # public, friends-only, private
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    author: Optional[User] = Relationship(back_populates="posts")


# ----------------------------------------
# Follow
# ----------------------------------------
class Follow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="user.id")
    following_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Friendship
# ----------------------------------------
class Friendship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    friend_id: int = Field(foreign_key="user.id")
    status: str  # requested, accepted, blocked
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Block
# ----------------------------------------
class Block(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    blocker_id: int = Field(foreign_key="user.id")
    blocked_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Comment
# ----------------------------------------
class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")
    content_text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Reaction
# ----------------------------------------
class Reaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")
    type: str  # like, upvote, etc.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Tag
# ----------------------------------------
class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


# ----------------------------------------
# PostTag (Many-to-many)
# ----------------------------------------
class PostTag(SQLModel, table=True):
    post_id: int = Field(foreign_key="post.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


# ----------------------------------------
# Category
# ----------------------------------------
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


# ----------------------------------------
# PostCategory (Many-to-many)
# ----------------------------------------
class PostCategory(SQLModel, table=True):
    post_id: int = Field(foreign_key="post.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)


# ------------- BELOWS ARE OPTIONAL -----------------

# ----------------------------------------
# View History
# ----------------------------------------
class UserPostViewHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    viewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# Notification
# ----------------------------------------
class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # recipient
    actor_id: int = Field(foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    type: str  # comment, reaction, follow, friend_request
    read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ----------------------------------------
# FriendRequest (Optional separation)
# ----------------------------------------
class FriendRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_user_id: int = Field(foreign_key="user.id")
    to_user_id: int = Field(foreign_key="user.id")
    status: str  # pending, accepted, declined
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
