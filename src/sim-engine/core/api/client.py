# api/client.py
import httpx

BASE_URL = "http://localhost:8000"  # your FastAPI server URL


class SocialAPIClient:
    def __init__(self, base_url=BASE_URL):
        self.client = httpx.Client(base_url=base_url)

    def create_post(self, user_id: str, content: str):
        response = self.client.post(
            "/posts/", json={"user_id": user_id, "content": content}
        )
        response.raise_for_status()
        return response.json()

    def get_feed(self, user_id: str):
        response = self.client.get(f"/feed/{user_id}")
        response.raise_for_status()
        return response.json()
