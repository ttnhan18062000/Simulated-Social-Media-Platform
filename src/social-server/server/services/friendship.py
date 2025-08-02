from typing import List
from sqlmodel import select
from server.db.models import Friendship
from server.db.session import get_session
from server.schemas.friendship import FriendshipCreate, FriendshipUpdate


async def create_friendship(data: FriendshipCreate):
    async with get_session() as session:
        friendship = Friendship(**data.model_dump())
        session.add(friendship)
        await session.commit()
        await session.refresh(friendship)
        return friendship


async def get_friendship_by_id(friendship_id: int):
    async with get_session() as session:
        result = await session.exec(
            select(Friendship).where(Friendship.id == friendship_id)
        )
        return result.first()


async def get_friendships_for_user(user_id: int) -> List[Friendship]:
    async with get_session() as session:
        result = await session.exec(
            select(Friendship).where(Friendship.user_id == user_id)
        )
        return result.all()


async def update_friendship(friendship_id: int, data: FriendshipUpdate):
    async with get_session() as session:
        result = await session.exec(
            select(Friendship).where(Friendship.id == friendship_id)
        )
        friendship = result.first()
        if not friendship:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(friendship, key, value)
        await session.commit()
        await session.refresh(friendship)
        return friendship


async def delete_friendship(friendship_id: int):
    async with get_session() as session:
        result = await session.exec(
            select(Friendship).where(Friendship.id == friendship_id)
        )
        friendship = result.first()
        if not friendship:
            return False
        await session.delete(friendship)
        await session.commit()
        return True
