import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.models import Follow
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_follow(mocker):
    payload = {"follower_id": 1, "following_id": 2}
    fake_follow = Follow(id=1, **payload)

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(obj):
        obj.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.follow.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/follows/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["follower_id"] == 1
        assert data["following_id"] == 2


@pytest.mark.asyncio
async def test_get_follow_by_id(mocker):
    fake_follow = Follow(id=1, follower_id=1, following_id=2)

    mock_result = MagicMock()
    mock_result.first.return_value = fake_follow

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.follow.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/follows/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["follower_id"] == 1


@pytest.mark.asyncio
async def test_get_followers(mocker):
    fake_follows = [Follow(id=1, follower_id=10, following_id=20)]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_follows

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.follow.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/follows/followers/20")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["following_id"] == 20


@pytest.mark.asyncio
async def test_get_followings(mocker):
    fake_follows = [Follow(id=2, follower_id=30, following_id=40)]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_follows

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.follow.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/follows/following/30")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["follower_id"] == 30


@pytest.mark.asyncio
async def test_delete_follow(mocker):
    fake_follow = Follow(id=1, follower_id=1, following_id=2)

    mock_result = MagicMock()
    mock_result.first.return_value = fake_follow

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    mocker.patch(
        "server.services.follow.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.delete("/api/v1/follows/1")
        assert resp.status_code == 204
        assert resp.content == b""
