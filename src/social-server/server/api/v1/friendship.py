from fastapi import APIRouter, HTTPException, status
from typing import List
from server.schemas.friendship import FriendshipCreate, FriendshipRead, FriendshipUpdate
from server.services.friendship import (
    create_friendship,
    get_friendship_by_id,
    get_friendships_for_user,
    update_friendship,
    delete_friendship,
)

router = APIRouter(prefix="/friendships", tags=["Friendships"])


@router.post("/", response_model=FriendshipRead)
async def create(friendship: FriendshipCreate):
    return await create_friendship(friendship)


@router.get("/{friendship_id}", response_model=FriendshipRead)
async def get_one(friendship_id: int):
    friendship = await get_friendship_by_id(friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return friendship


@router.get("/by-user/{user_id}", response_model=List[FriendshipRead])
async def get_by_user(user_id: int):
    return await get_friendships_for_user(user_id)


@router.put("/{friendship_id}", response_model=FriendshipRead)
async def update(friendship_id: int, data: FriendshipUpdate):
    updated = await update_friendship(friendship_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return updated


@router.delete("/{friendship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(friendship_id: int):
    deleted = await delete_friendship(friendship_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Friendship not found")
