from fastapi import APIRouter, HTTPException, status
from typing import List
from server.schemas.user_feed import UserFeedCreate, UserFeedRead, UserFeedUpdate
from server.services.user_feed import (
    create_user_feed,
    get_user_feed_by_id,
    get_feeds_for_user,
    update_user_feed,
    delete_user_feed,
)

router = APIRouter(prefix="/user-feeds", tags=["UserFeeds"])


@router.post("/", response_model=UserFeedRead)
async def create(feed: UserFeedCreate):
    return await create_user_feed(feed)


@router.get("/{feed_id}", response_model=UserFeedRead)
async def get_one(feed_id: int):
    feed = await get_user_feed_by_id(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feed


@router.get("/by-user/{user_id}", response_model=List[UserFeedRead])
async def get_by_user(user_id: int):
    return await get_feeds_for_user(user_id)


@router.put("/{feed_id}", response_model=UserFeedRead)
async def update(feed_id: int, feed: UserFeedUpdate):
    updated = await update_user_feed(feed_id, feed)
    if not updated:
        raise HTTPException(status_code=404, detail="Feed not found")
    return updated


@router.delete("/{feed_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(feed_id: int):
    deleted = await delete_user_feed(feed_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Feed not found")
