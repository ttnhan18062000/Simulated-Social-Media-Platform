from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.api.v1 import user, post
from server.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (if needed)


app = FastAPI(
    title="User Service API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(post.router, prefix="/api/v1")
