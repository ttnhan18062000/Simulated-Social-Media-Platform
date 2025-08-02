import pytest
from httpx import AsyncClient, ASGITransport
from server import app
from server.db.models import Reaction
from unittest.mock import MagicMock, AsyncMock
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_reaction(mocker):
    payload = {"post_id": 1, "user_id": 42, "type": "like"}

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(obj):
        obj.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.reaction.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/reactions/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["type"] == "like"


@pytest.mark.asyncio
async def test_get_reactions_for_post(mocker):
    fake_reactions = [
        Reaction(
            id=1, post_id=1, user_id=42, type="like", created_at="2025-08-01T00:00:00Z"
        )
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_reactions

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.reaction.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/reactions/post/1")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["type"] == "like"
