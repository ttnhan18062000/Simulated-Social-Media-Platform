# agents/tools.py
import httpx

BASE_URL = "http://localhost:8888/api/v1"
client = httpx.Client(base_url=BASE_URL)


def create_post(user_id: int, content_text: str, visibility="public", image_url=None):
    payload = {
        "user_id": user_id,
        "content_text": content_text,
        "visibility": visibility,
    }
    if image_url:
        payload["image_url"] = image_url

    res = client.post("/posts/", json=payload)
    res.raise_for_status()
    return res.json()


def create_comment(post_id: int, user_id: int, content_text: str):
    payload = {
        "post_id": post_id,
        "user_id": user_id,
        "content_text": content_text,
    }
    res = client.post("/comments/", json=payload)
    res.raise_for_status()
    return res.json()


def create_reaction(post_id: int, user_id: int, reaction_type: str):
    payload = {
        "post_id": post_id,
        "user_id": user_id,
        "type": reaction_type,  # e.g., "like"
    }
    res = client.post("/reactions/", json=payload)
    res.raise_for_status()
    return res.json()


def get_feed(user_id: int) -> list:
    res = client.get(f"/feed/{user_id}")
    res.raise_for_status()
    return res.json()
