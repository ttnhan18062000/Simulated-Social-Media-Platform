from fastapi import APIRouter, HTTPException, status
from typing import List
from server.schemas.follow import FollowCreate, FollowRead
from server.services.follow import (
    create_follow,
    get_follow_by_id,
    get_followers,
    get_followings,
    delete_follow,
)

router = APIRouter(prefix="/follows", tags=["Follows"])


@router.post("/", response_model=FollowRead)
async def create(follow: FollowCreate):
    return await create_follow(follow)


@router.get("/{follow_id}", response_model=FollowRead)
async def get_one(follow_id: int):
    follow = await get_follow_by_id(follow_id)
    if not follow:
        raise HTTPException(status_code=404, detail="Follow not found")
    return follow


@router.get("/followers/{user_id}", response_model=List[FollowRead])
async def get_user_followers(user_id: int):
    return await get_followers(user_id)


@router.get("/following/{user_id}", response_model=List[FollowRead])
async def get_user_followings(user_id: int):
    return await get_followings(user_id)


@router.delete("/{follow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(follow_id: int):
    deleted = await delete_follow(follow_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Follow not found")
