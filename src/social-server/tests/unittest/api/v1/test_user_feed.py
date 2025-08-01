import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.models import UserFeed
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_user_feed(mocker):
    payload = {"user_id": 1, "post_id": 42}
    fake_feed = UserFeed(id=1, **payload)

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(feed):
        feed.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.user_feed.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/user-feeds/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == 1
        assert data["post_id"] == 42


@pytest.mark.asyncio
async def test_get_user_feed_by_id(mocker):
    fake_feed = UserFeed(id=1, user_id=2, post_id=42)

    mock_result = MagicMock()
    mock_result.first.return_value = fake_feed

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.user_feed.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/user-feeds/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["user_id"] == 2
        assert data["post_id"] == 42


@pytest.mark.asyncio
async def test_get_user_feeds_by_user(mocker):
    fake_feeds = [
        UserFeed(id=1, user_id=10, post_id=100),
        UserFeed(id=2, user_id=10, post_id=101),
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_feeds

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.user_feed.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/user-feeds/by-user/10")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all(feed["user_id"] == 10 for feed in data)


@pytest.mark.asyncio
async def test_update_user_feed(mocker):
    fake_feed = UserFeed(id=1, user_id=5, post_id=50, is_seen=False)
    updated_fields = {"is_seen": True}

    mock_result = MagicMock()
    mock_result.first.return_value = fake_feed

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    mocker.patch(
        "server.services.user_feed.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.put("/api/v1/user-feeds/1", json=updated_fields)
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_seen"] is True


@pytest.mark.asyncio
async def test_delete_user_feed(mocker):
    fake_feed = UserFeed(id=1, user_id=1, post_id=1)

    mock_result = MagicMock()
    mock_result.first.return_value = fake_feed

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    mocker.patch(
        "server.services.user_feed.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.delete("/api/v1/user-feeds/1")
        assert resp.status_code == 204
        assert resp.content == b""
