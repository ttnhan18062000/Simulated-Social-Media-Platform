import pytest
from httpx import AsyncClient, ASGITransport
from server import app
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_category():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post(
            "/api/v1/categories/",
            json={"name": "Tech", "description": "Technology and programming stuff"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Tech"


@pytest.mark.asyncio
async def test_assign_category_to_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        category_resp = await ac.post(
            "/api/v1/categories/",
            json={"name": "Lifestyle", "description": "Life tips and self-care"},
        )
        category_id = category_resp.json()["id"]

        assign_resp = await ac.post(
            "/api/v1/categories/assign", json={"post_id": 1, "category_id": category_id}
        )
        assert assign_resp.status_code == 200
        assert assign_resp.json()["post_id"] == 1
