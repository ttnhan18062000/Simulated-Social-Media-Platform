from fastapi import APIRouter, HTTPException
from server.schemas.user import UserCreate, UserRead
from server.services.user_service import create_user, get_user

router = APIRouter()


@router.post("/", response_model=UserRead)
async def create(user: UserCreate):
    return await create_user(user)


@router.get("/{user_id}", response_model=UserRead)
async def read(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
