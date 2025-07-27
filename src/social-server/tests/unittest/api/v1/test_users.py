import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from server import app
from server.db.session import get_session
from server.db.models.user import User


@pytest.mark.asyncio
async def test_create_user(mocker):
    # Fake user input + expected output
    payload = {"name": "Nate", "email": "nate@test.com", "password": "123"}
    fake_user = User(id=1, **payload, created_at="2024-01-01T00:00:00")

    # Mock session methods
    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Add refresh side effect to set .id
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
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/api/v1/users/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nate"
        assert data["email"] == "nate@test.com"
        assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_all_users(mocker):
    # Create fake user return values
    fake_users = [
        User(
            id=1,
            name="Nate",
            email="nate@test.com",
            password="123",
            created_at="2024-01-01T00:00:00",
        ),
        User(
            id=2,
            name="Jane",
            email="jane@test.com",
            password="456",
            created_at="2024-01-02T00:00:00",
        ),
    ]

    # Mock session + exec
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
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        resp = await ac.get("/api/v1/users/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["name"] == "Nate"


@pytest.mark.asyncio
async def test_get_user_by_id(mocker):
    fake_user = User(
        id=1,
        name="Nate",
        email="nate@test.com",
        password="123",
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
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        resp = await ac.get("/api/v1/users/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["name"] == "Nate"


@pytest.mark.asyncio
async def test_update_user(mocker):
    # Simulate a user before update
    fake_user = User(
        id=1,
        name="Nate",
        email="nate@test.com",
        password="123",
        created_at="2025-01-01T00:00:00Z",
    )

    # Expected updated fields
    updated_fields = {"name": "Nate Updated"}
    updated_user = User(
        id=1,
        name="Nate Updated",
        email="nate@test.com",  # email unchanged
        password="123",
        created_at="2025-01-01T00:00:00Z",
    )

    # Mock result.exec().first() to simulate SELECT returning existing user
    mock_result = MagicMock()
    mock_result.first.return_value = fake_user

    # Mock session
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
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        resp = await ac.put("/api/v1/users/1", json=updated_fields)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nate Updated"
        assert data["id"] == 1


@pytest.mark.asyncio
async def test_delete_user(mocker):
    fake_user = User(
        id=1,
        name="Nate",
        email="nate@test.com",
        password="123",
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
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        resp = await ac.delete("/api/v1/users/1")
        assert resp.status_code == 204
        assert resp.content == b""
