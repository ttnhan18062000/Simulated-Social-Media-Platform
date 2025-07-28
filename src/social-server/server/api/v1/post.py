from fastapi import APIRouter, HTTPException, status
from server.schemas.post import PostCreate, PostRead, PostUpdate
from server.services.post import (
    create_post,
    get_all_posts,
    get_post_by_id,
    update_post,
    delete_post,
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostRead)
async def create(post: PostCreate):
    return await create_post(post)


@router.get("/", response_model=list[PostRead])
async def get_all():
    return await get_all_posts()


@router.get("/{post_id}", response_model=PostRead)
async def get_one(post_id: int):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostRead)
async def update(post_id: int, post: PostUpdate):
    updated = await update_post(post_id, post)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post_id: int):
    deleted = await delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
