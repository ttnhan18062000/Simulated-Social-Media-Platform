import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.models import User
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_user(mocker):
    payload = {"username": "Nate", "password": "123"}
    fake_user = User(
        id=1,
        username="Nate",
        password_hash="123",
        created_at="2024-01-01T00:00:00",
    )

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    async def fake_refresh(user):
        user.id = 1

    mock_session.refresh.side_effect = fake_refresh

    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/users/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "Nate"
        assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_all_users(mocker):
    fake_users = [
        User(
            id=1,
            username="Nate",
            password_hash="123",
            created_at="2024-01-01T00:00:00",
        ),
        User(
            id=2,
            username="Jane",
            password_hash="456",
            created_at="2024-01-02T00:00:00",
        ),
    ]

    mock_result = MagicMock()
    mock_result.all.return_value = fake_users

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/users/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["username"] == "Nate"


@pytest.mark.asyncio
async def test_get_user_by_id(mocker):
    fake_user = User(
        id=1,
        username="Nate",
        password_hash="123",
        created_at="2024-01-01T00:00:00",
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_user

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/users/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["username"] == "Nate"


@pytest.mark.asyncio
async def test_update_user(mocker):
    fake_user = User(
        id=1,
        username="Nate",
        password_hash="123",
        created_at="2025-01-01T00:00:00Z",
    )
    updated_fields = {"username": "Nate Updated"}

    mock_result = MagicMock()
    mock_result.first.return_value = fake_user

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.put("/api/v1/users/1", json=updated_fields)
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "Nate Updated"
        assert data["id"] == 1


@pytest.mark.asyncio
async def test_delete_user(mocker):
    fake_user = User(
        id=1,
        username="Nate",
        password_hash="123",
        created_at="2024-01-01T00:00:00Z",
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_user

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.delete("/api/v1/users/1")
        assert resp.status_code == 204
        assert resp.content == b""


@pytest.mark.asyncio
async def test_get_user_with_posts(mocker):
    from server.db.models import User, Post

    fake_user = User(
        id=1,
        username="nini",
        password_hash="secret",
        created_at="2025-01-01T00:00:00",
        posts=[
            Post(
                id=1,
                user_id=1,
                content_text="Hello world!",
                visibility="public",
                created_at="2025-01-01T00:00:00",
            ),
            Post(
                id=2,
                user_id=1,
                content_text="Another post",
                visibility="friends-only",
                created_at="2025-01-02T00:00:00",
            ),
        ],
    )

    mock_result = MagicMock()
    mock_result.first.return_value = fake_user

    mock_session = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_result)

    mocker.patch(
        "server.services.user.get_session",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock()
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.get("/api/v1/users/1/with-posts")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["username"] == "nini"
        assert len(data["posts"]) == 2
        assert data["posts"][0]["content_text"] == "Hello world!"
