from fastapi import APIRouter, HTTPException
from typing import List
from server.schemas.comment import CommentCreate, CommentRead
from server.services.comment import create_comment, get_comments_for_post

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentRead)
async def create(comment: CommentCreate):
    return await create_comment(comment)


@router.get("/post/{post_id}", response_model=List[CommentRead])
async def get_post_comments(post_id: int):
    comments = await get_comments_for_post(post_id)
    if comments is None:
        raise HTTPException(status_code=404, detail="No comments found for this post")
    return comments
