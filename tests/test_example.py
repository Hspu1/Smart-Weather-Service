import pytest


@pytest.mark.asyncio
async def test_get_message(async_client):
    response = await async_client.get("/get-message")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
