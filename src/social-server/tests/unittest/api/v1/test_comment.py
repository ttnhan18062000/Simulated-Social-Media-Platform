import pytest
from httpx import AsyncClient, ASGITransport
from server import app
from server.db.models import Comment
from unittest.mock import MagicMock, AsyncMock
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_comment(mocker):
    payload = {"post_id": 1, "user_id": 2, "content_text": "Nice post!"}

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(obj):
        obj.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.comment.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/comments/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["content_text"] == "Nice post!"


@pytest.mark.asyncio
async def test_get_post_comments(mocker):
    fake_comments = [
        Comment(
            id=1,
            post_id=1,
            user_id=2,
            content_text="Nice!",
            created_at="2025-08-01T00:00:00Z",
        )
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_comments

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.comment.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/comments/post/1")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["post_id"] == 1
