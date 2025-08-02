from sqlmodel import select
from server.db.models import Tag, PostTag
from server.db.session import get_session
from server.schemas.tag import TagCreate
from typing import List


async def create_tag(data: TagCreate) -> Tag:
    async with get_session() as session:
        tag = Tag(**data.model_dump())
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag


async def get_all_tags() -> List[Tag]:
    async with get_session() as session:
        result = await session.exec(select(Tag))
        return result.all()
