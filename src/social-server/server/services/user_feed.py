from server.db.models import UserFeed
from server.db.session import get_session
from server.schemas.user_feed import UserFeedCreate, UserFeedUpdate
from sqlmodel import select
from datetime import datetime
from typing import List


async def create_user_feed(feed_data: UserFeedCreate):
    async with get_session() as session:
        new_feed = UserFeed(**feed_data.model_dump())
        session.add(new_feed)
        await session.commit()
        await session.refresh(new_feed)
        return new_feed


async def get_user_feed_by_id(feed_id: int):
    async with get_session() as session:
        result = await session.exec(select(UserFeed).where(UserFeed.id == feed_id))
        return result.first()


async def get_feeds_for_user(user_id: int) -> List[UserFeed]:
    async with get_session() as session:
        result = await session.exec(
            select(UserFeed)
            .where(UserFeed.user_id == user_id)
            .order_by(UserFeed.added_at.desc())
        )
        return result.all()


async def update_user_feed(feed_id: int, feed_data: UserFeedUpdate):
    async with get_session() as session:
        result = await session.exec(select(UserFeed).where(UserFeed.id == feed_id))
        feed = result.first()
        if not feed:
            return None
        for key, value in feed_data.model_dump(exclude_unset=True).items():
            setattr(feed, key, value)
        await session.commit()
        await session.refresh(feed)
        return feed


async def delete_user_feed(feed_id: int):
    async with get_session() as session:
        result = await session.exec(select(UserFeed).where(UserFeed.id == feed_id))
        feed = result.first()
        if not feed:
            return False
        await session.delete(feed)
        await session.commit()
        return True
