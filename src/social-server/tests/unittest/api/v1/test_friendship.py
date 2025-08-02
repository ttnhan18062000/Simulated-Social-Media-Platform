import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.models import Friendship
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_friendship(mocker):
    payload = {"user_id": 1, "friend_id": 2, "status": "requested"}
    fake_friendship = Friendship(id=1, **payload)

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(obj):
        obj.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.friendship.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/friendships/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "requested"
        assert data["user_id"] == 1
        assert data["friend_id"] == 2


@pytest.mark.asyncio
async def test_get_friendship_by_id(mocker):
    fake_friendship = Friendship(id=1, user_id=1, friend_id=2, status="accepted")

    mock_result = MagicMock()
    mock_result.first.return_value = fake_friendship

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.friendship.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/friendships/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "accepted"


@pytest.mark.asyncio
async def test_get_friendships_for_user(mocker):
    fake_friendships = [
        Friendship(id=1, user_id=10, friend_id=11, status="accepted"),
        Friendship(id=2, user_id=10, friend_id=12, status="requested"),
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_friendships

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.friendship.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/friendships/by-user/10")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all(f["user_id"] == 10 for f in data)


@pytest.mark.asyncio
async def test_update_friendship(mocker):
    fake_friendship = Friendship(id=1, user_id=1, friend_id=2, status="requested")
    updated_fields = {"status": "accepted"}

    mock_result = MagicMock()
    mock_result.first.return_value = fake_friendship

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    mocker.patch(
        "server.services.friendship.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.put("/api/v1/friendships/1", json=updated_fields)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "accepted"


@pytest.mark.asyncio
async def test_delete_friendship(mocker):
    fake_friendship = Friendship(id=1, user_id=1, friend_id=2, status="requested")

    mock_result = MagicMock()
    mock_result.first.return_value = fake_friendship

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    mocker.patch(
        "server.services.friendship.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.delete("/api/v1/friendships/1")
        assert resp.status_code == 204
        assert resp.content == b""
