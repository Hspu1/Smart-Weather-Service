from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker


backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
broker = RedisStreamBroker(
    url="redis://localhost:6379/1"
).with_result_backend(result_backend=backend)

redis_cache = Redis(
    host="127.0.0.1", port=6379, decode_responses=True, db=2
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()

    await redis_cache.ping()
    app.state.redis_cache = redis_cache

    yield

    if not broker.is_worker_process:
        await broker.shutdown()
    await app.state.redis_cache.aclose()
