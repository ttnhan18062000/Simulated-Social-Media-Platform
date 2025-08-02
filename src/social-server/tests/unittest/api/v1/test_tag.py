import pytest
from httpx import AsyncClient, ASGITransport
from server import app
from server.common.config import base_url


@pytest.mark.asyncio
async def test_create_tag():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        resp = await ac.post("/api/v1/tags/", json={"name": "funny"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "funny"


@pytest.mark.asyncio
async def test_assign_tag_to_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        tag_resp = await ac.post("/api/v1/tags/", json={"name": "drama"})
        tag_id = tag_resp.json()["id"]

        resp = await ac.post(
            "/api/v1/tags/assign", json={"post_id": 1, "tag_id": tag_id}
        )
        assert resp.status_code == 200
        assert resp.json()["post_id"] == 1
