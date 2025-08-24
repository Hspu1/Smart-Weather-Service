import pytest
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport

from app.main import app


# тестируемый эндпоинт:
# @app.get(path="/get-message", status_code=200)
# async def get_message() -> dict[str, str]:
#     return {
#         "message": "Hello World"
#     }


@fixture(loop_scope="function")
async def async_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_get_message(async_client):
    response = await async_client.get("/get-message")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
