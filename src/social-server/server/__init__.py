from fastapi import FastAPI
from server.api.v1.user import user

app = FastAPI(title="User Service API", version="1.0.0")

app.include_router(user.router, prefix="/api/v1/users")
