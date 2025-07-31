from sqlmodel import select
from server.db.models import Post
from server.db.session import get_session  # reuse existing get_session
from server.schemas.post import PostCreate, PostUpdate


async def create_post(post_data: PostCreate):
    async with get_session() as session:
        new_post = Post(**post_data.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post


async def get_post_by_id(post_id: int):
    async with get_session() as session:
        result = await session.exec(select(Post).where(Post.id == post_id))
        return result.first()


async def get_all_posts():
    async with get_session() as session:
        result = await session.exec(select(Post))
        return result.all()


async def update_post(post_id: int, post_data: PostUpdate):
    async with get_session() as session:
        result = await session.exec(select(Post).where(Post.id == post_id))
        post = result.first()
        if not post:
            return None
        for key, value in post_data.model_dump(exclude_unset=True).items():
            setattr(post, key, value)
        await session.commit()
        await session.refresh(post)
        return post


async def delete_post(post_id: int):
    async with get_session() as session:
        result = await session.exec(select(Post).where(Post.id == post_id))
        post = result.first()
        if not post:
            return False
        await session.delete(post)
        await session.commit()
        return True
