from typing import List
from sqlmodel import select
from server.db.models import Follow
from server.db.session import get_session
from server.schemas.follow import FollowCreate


async def create_follow(follow_data: FollowCreate):
    async with get_session() as session:
        new_follow = Follow(**follow_data.model_dump())
        session.add(new_follow)
        await session.commit()
        await session.refresh(new_follow)
        return new_follow


async def get_follow_by_id(follow_id: int):
    async with get_session() as session:
        result = await session.exec(select(Follow).where(Follow.id == follow_id))
        return result.first()


async def get_followers(user_id: int) -> List[Follow]:
    async with get_session() as session:
        result = await session.exec(
            select(Follow).where(Follow.following_id == user_id)
        )
        return result.all()


async def get_followings(user_id: int) -> List[Follow]:
    async with get_session() as session:
        result = await session.exec(select(Follow).where(Follow.follower_id == user_id))
        return result.all()


async def delete_follow(follow_id: int):
    async with get_session() as session:
        result = await session.exec(select(Follow).where(Follow.id == follow_id))
        follow = result.first()
        if not follow:
            return False
        await session.delete(follow)
        await session.commit()
        return True
