import pytest
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport

from app.main import app


@fixture(loop_scope="function")
async def async_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client
