import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.models import Post
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_post(mocker):
    payload = {"content": "My first post", "user_id": 1}
    fake_post = Post(id=1, **payload, created_at="2025-01-01T00:00:00")

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(post):
        post.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.post.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/posts/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "My first post"
        assert data["id"] == 1
        assert data["user_id"] == 1


@pytest.mark.asyncio
async def test_get_all_posts(mocker):
    fake_posts = [
        Post(
            id=1,
            content="Content 1",
            user_id=1,
            created_at="2025-01-01T00:00:00",
        ),
        Post(
            id=2,
            content="Content 2",
            user_id=2,
            created_at="2025-01-02T00:00:00",
        ),
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_posts

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.post.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/posts/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["content"] == "Content 1"


@pytest.mark.asyncio
async def test_get_post_by_id(mocker):
    fake_post = Post(
        id=1,
        content="Lone content",
        user_id=1,
        created_at="2025-01-01T00:00:00",
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_post

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.post.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/posts/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["user_id"] == 1
        assert data["content"] == "Lone content"


@pytest.mark.asyncio
async def test_update_post(mocker):
    fake_post = Post(
        id=1,
        content="Old Content",
        user_id=1,
        created_at="2025-01-01T00:00:00",
    )
    updated_fields = {"content": "New Content"}
    updated_post = Post(
        id=1,
        content="New Content",
        user_id=1,
        created_at="2025-01-01T00:00:00",
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_post

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    mocker.patch(
        "server.services.post.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.put("/api/v1/posts/1", json=updated_fields)
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "New Content"


@pytest.mark.asyncio
async def test_delete_post(mocker):
    fake_post = Post(
        id=1,
        content="Bye!",
        user_id=1,
        created_at="2025-01-01T00:00:00",
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_post

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    mocker.patch(
        "server.services.post.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.delete("/api/v1/posts/1")
        assert resp.status_code == 204
        assert resp.content == b""
