from fastapi import APIRouter, HTTPException, status
from typing import List
from server.schemas.user import UserCreate, UserRead, UserUpdate
from server.services.user import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
async def create(user: UserCreate):
    return await create_user(user)


@router.get("/", response_model=List[UserRead])
async def read_all_users():
    return await get_all_users()


@router.get("/{user_id}", response_model=UserRead)
async def read(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update(user_id: int, user: UserUpdate):
    updated = await update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int):
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
