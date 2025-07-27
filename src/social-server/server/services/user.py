from server.db.models.user import User
from server.db.session import get_session
from server.schemas.user import UserCreate, UserUpdate
from sqlmodel import select
from datetime import datetime
from typing import List


async def create_user(user_data: UserCreate) -> User:
    async with get_session() as session:
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            created_at=datetime.utcnow().isoformat(),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def get_all_users() -> List[User]:
    async with get_session() as session:
        users = await session.exec(select(User))
        return users.all()


async def get_user(user_id: int) -> User | None:
    async with get_session() as session:
        result = await session.exec(select(User).where(User.id == user_id))
        return result.first()


async def update_user(user_id: int, user_data: UserUpdate) -> User | None:
    async with get_session() as session:
        result = await session.exec(select(User).where(User.id == user_id))
        user = result.first()
        if not user:
            return None

        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)
        return user


async def delete_user(user_id: int) -> bool:
    async with get_session() as session:
        result = await session.exec(select(User).where(User.id == user_id))
        user = result.first()
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True
