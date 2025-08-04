from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite+aiosqlite:///./simengine.db"
DB_FILE = "./simengine.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=SQLModelAsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
