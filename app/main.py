import uvicorn

from app.tasks.crud_tasks import router as crud_tasks_router
from app.auth.auth import router as auth_router
from app.categories.crud_categories import router as categories_router
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]: # Настройка до запуска приложения
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(crud_tasks_router)
app.include_router(categories_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

