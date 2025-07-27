from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.api.v1.user import router as user_router
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

app.include_router(user_router, prefix="/api/v1/users")
