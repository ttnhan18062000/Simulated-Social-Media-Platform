from sqlmodel import select
from typing import List
from server.db.models import Category
from server.schemas.category import CategoryCreate
from server.db.session import get_session


async def create_category(data: CategoryCreate) -> Category:
    async with get_session() as session:
        category = Category(**data.model_dump())
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


async def get_all_categories() -> List[Category]:
    async with get_session() as session:
        result = await session.exec(select(Category))
        return result.all()
