from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ----------------------------------------
# Core SimUser Table
# ----------------------------------------
class SimUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # references real User.id
    memory_key: Optional[str] = None  # RAG reference
    tick_count: int = 0
    cooldown_until: Optional[datetime] = None

    # Relationships
    persona: Optional["PersonaProfile"] = Relationship(back_populates="sim_user")
    mental_state: Optional["UserMentalState"] = Relationship(back_populates="sim_user")
    actions: List["UserActionHistory"] = Relationship(back_populates="sim_user")
    reflections: List["UserReflection"] = Relationship(back_populates="sim_user")
    relationships: List["UserRelationship"] = Relationship(back_populates="sim_user")
    preferences: Optional["UserPreference"] = Relationship(back_populates="sim_user")
    tags: List["UserTraitTag"] = Relationship(back_populates="sim_user")


# ----------------------------------------
# Persona Profile (1:1)
# ----------------------------------------
class PersonaProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id", unique=True)

    full_name: Optional[str]
    age: Optional[int]
    location: Optional[str]
    occupation: Optional[str]
    writing_style: Optional[str]
    hobbies: Optional[str]  # could be list[str] in JSON
    values: Optional[str]
    personality_traits: Optional[str]  # JSON string or comma-separated

    sim_user: Optional[SimUser] = Relationship(back_populates="persona")


# ----------------------------------------
# Mental State (1:1)
# ----------------------------------------
class UserMentalState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id", unique=True)

    mood: Optional[str]
    energy_level: Optional[str]
    obsession_topic: Optional[str]
    focus_level: Optional[str]
    time_of_day_state: Optional[str]  # e.g., “morning”, “evening”

    sim_user: Optional[SimUser] = Relationship(back_populates="mental_state")


# ----------------------------------------
# User Action History (1:N)
# ----------------------------------------
class UserActionHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id")

    action_type: str  # post, comment, like, follow, etc.
    goal: Optional[str]
    content_summary: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    sim_user: Optional[SimUser] = Relationship(back_populates="actions")


# ----------------------------------------
# User Reflection (1:N)
# ----------------------------------------
class UserReflection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id")

    reflection_text: str
    related_action_ids: Optional[str]  # comma-separated IDs or summary
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: Optional[str]  # e.g., “weekly”, “post-reaction”

    sim_user: Optional[SimUser] = Relationship(back_populates="reflections")


# ----------------------------------------
# User Relationship (1:N)
# ----------------------------------------
class UserRelationship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id")
    target_user_id: int  # ID from the real User table

    strength: float = 0.0
    sentiment: Optional[str]  # e.g., “positive”, “negative”, “conflicted”
    tags: Optional[str]  # e.g., “friend”, “rival”, “troll”

    sim_user: Optional[SimUser] = Relationship(back_populates="relationships")


# ----------------------------------------
# User Preference (1:1 or 1:N)
# ----------------------------------------
class UserPreference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id", unique=True)

    preferred_topics: Optional[str]
    tone: Optional[str]
    use_emojis: Optional[bool] = True
    post_length_style: Optional[str]  # short, medium, long

    sim_user: Optional[SimUser] = Relationship(back_populates="preferences")


# ----------------------------------------
# Trait Tags (1:N)
# ----------------------------------------
class UserTraitTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sim_user_id: int = Field(foreign_key="simuser.id")

    name: str  # e.g., “introvert”, “group_A”
    value: Optional[str]

    sim_user: Optional[SimUser] = Relationship(back_populates="tags")
