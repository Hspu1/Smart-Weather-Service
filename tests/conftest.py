from unittest.mock import AsyncMock

from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from taskiq import TaskiqResult

from app.core.lifespan import broker
from app.main import app


@fixture(loop_scope="function")
async def async_client():
    """Mок HTTP клиента"""
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@fixture(scope="function")
async def broker_backend():
    """Мок бэкенда брокера"""
    original_backend = broker.result_backend
    mock_backend = AsyncMock()

    mock_result = TaskiqResult(
        is_err=False,
        return_value={"temperature": 20, "condition": "sunny"},
        execution_time=0.01
    )
    mock_backend.get_result = AsyncMock(return_value=mock_result)
    broker.result_backend = mock_backend

    yield broker.result_backend

    broker.result_backend = original_backend
