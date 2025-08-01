from sqlmodel import select
from server.db.models import Comment
from server.db.session import get_session
from server.schemas.comment import CommentCreate


async def create_comment(comment_data: CommentCreate):
    async with get_session() as session:
        comment = Comment(**comment_data.model_dump())
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment


async def get_comments_for_post(post_id: int):
    async with get_session() as session:
        result = await session.exec(
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at)
        )
        return result.all()
