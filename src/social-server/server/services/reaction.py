from sqlmodel import select
from server.db.models import Reaction
from server.db.session import get_session
from server.schemas.reaction import ReactionCreate


async def create_reaction(data: ReactionCreate):
    async with get_session() as session:
        reaction = Reaction(**data.model_dump())
        session.add(reaction)
        await session.commit()
        await session.refresh(reaction)
        return reaction


async def get_reactions_for_post(post_id: int):
    async with get_session() as session:
        result = await session.exec(select(Reaction).where(Reaction.post_id == post_id))
        return result.all()
