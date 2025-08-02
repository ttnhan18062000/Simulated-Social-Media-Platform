from sqlmodel import select
from typing import List
from server.db.models import PostCategory, Category
from server.db.session import get_session
from server.schemas.post_category import PostCategoryCreate


async def assign_category_to_post(data: PostCategoryCreate) -> PostCategory:
    async with get_session() as session:
        relation = PostCategory(**data.model_dump())
        session.add(relation)
        await session.commit()
        return relation


async def get_categories_for_post(post_id: int) -> List[Category]:
    async with get_session() as session:
        result = await session.exec(
            select(Category)
            .join(PostCategory, PostCategory.category_id == Category.id)
            .where(PostCategory.post_id == post_id)
        )
        return result.all()


async def get_post_ids_by_category(category_id: int) -> List[int]:
    async with get_session() as session:
        result = await session.exec(
            select(PostCategory.post_id).where(PostCategory.category_id == category_id)
        )
        return result.all()


async def add_category_to_post(data: PostCategoryCreate):
    async with get_session() as session:
        existing = await session.exec(
            select(PostCategory).where(
                (PostCategory.post_id == data.post_id)
                & (PostCategory.category_id == data.category_id)
            )
        )
        if existing.first():
            return  # avoid duplicate

        post_category = PostCategory(**data.dict())
        session.add(post_category)
        await session.commit()
