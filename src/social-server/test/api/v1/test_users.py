import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/users/", json={"name": "Nate", "email": "nate@test.com"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Nate"
