from fastapi import APIRouter
from typing import List
from server.schemas.tag import TagCreate, TagRead
from server.schemas.post_tag import PostTagCreate, PostTagRead
from server.services.tag import create_tag, get_all_tags
from server.services.post_tag import tag_post, get_tags_for_post, get_post_ids_by_tag

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagRead)
async def create(data: TagCreate):
    return await create_tag(data)


@router.get("/", response_model=List[TagRead])
async def all_tags():
    return await get_all_tags()


@router.post("/assign", response_model=PostTagRead)
async def assign_tag(data: PostTagCreate):
    return await tag_post(data)


@router.get("/post/{post_id}", response_model=List[TagRead])
async def get_tags(post_id: int):
    return await get_tags_for_post(post_id)


@router.get("/tag/{tag_id}/posts", response_model=List[int])
async def posts_by_tag(tag_id: int):
    return await get_post_ids_by_tag(tag_id)
