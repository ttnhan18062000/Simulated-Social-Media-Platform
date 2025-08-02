from sqlmodel import select
from server.db.models import PostTag, Tag
from server.db.session import get_session
from server.schemas.post_tag import PostTagCreate
from typing import List


async def tag_post(data: PostTagCreate) -> PostTag:
    async with get_session() as session:
        post_tag = PostTag(**data.model_dump())
        session.add(post_tag)
        await session.commit()
        return post_tag


async def get_tags_for_post(post_id: int) -> List[Tag]:
    async with get_session() as session:
        result = await session.exec(
            select(Tag)
            .join(PostTag, PostTag.tag_id == Tag.id)
            .where(PostTag.post_id == post_id)
        )
        return result.all()


async def get_post_ids_by_tag(tag_id: int) -> List[int]:
    async with get_session() as session:
        result = await session.exec(
            select(PostTag.post_id).where(PostTag.tag_id == tag_id)
        )
        return result.all()


async def add_tag_to_post(data: PostTagCreate):
    async with get_session() as session:
        # Optional: prevent duplicate entries
        existing = await session.exec(
            select(PostTag).where(
                (PostTag.post_id == data.post_id) & (PostTag.tag_id == data.tag_id)
            )
        )
        if existing.first():
            return  # skip duplicate

        post_tag = PostTag(**data.dict())
        session.add(post_tag)
        await session.commit()
