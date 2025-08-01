from fastapi import APIRouter, HTTPException
from typing import List
from server.schemas.reaction import ReactionCreate, ReactionRead
from server.services.reaction import create_reaction, get_reactions_for_post

router = APIRouter(prefix="/reactions", tags=["Reactions"])


@router.post("/", response_model=ReactionRead)
async def react(data: ReactionCreate):
    return await create_reaction(data)


@router.get("/post/{post_id}", response_model=List[ReactionRead])
async def get_post_reactions(post_id: int):
    reactions = await get_reactions_for_post(post_id)
    if not reactions:
        raise HTTPException(status_code=404, detail="No reactions found for this post")
    return reactions
