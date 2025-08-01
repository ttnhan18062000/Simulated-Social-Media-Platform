from fastapi import APIRouter
from typing import List
from server.schemas.category import CategoryCreate, CategoryRead
from server.schemas.post_category import PostCategoryCreate, PostCategoryRead
from server.services.category import create_category, get_all_categories
from server.services.post_category import (
    assign_category_to_post,
    get_categories_for_post,
    get_post_ids_by_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead)
async def create(data: CategoryCreate):
    return await create_category(data)


@router.get("/", response_model=List[CategoryRead])
async def list_all():
    return await get_all_categories()


@router.post("/assign", response_model=PostCategoryRead)
async def assign(data: PostCategoryCreate):
    return await assign_category_to_post(data)


@router.get("/post/{post_id}", response_model=List[CategoryRead])
async def get_categories(post_id: int):
    return await get_categories_for_post(post_id)


@router.get("/category/{category_id}/posts", response_model=List[int])
async def posts_by_category(category_id: int):
    return await get_post_ids_by_category(category_id)
