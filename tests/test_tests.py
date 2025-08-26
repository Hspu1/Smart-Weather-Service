import pytest


@pytest.mark.asyncio
async def test_get_weather(async_client):
    test_cases = [
        (40.7128, -74.0060),  # Нью-Йорк, США
        (4.7110, -74.0721),  # Богота, Колумбия
        (-23.5505, -46.6333),  # Сан-Паулу, Бразилия
        (55.7558, 37.6173),  # Москва, Россия
        (48.8566, 2.3522),  # Париж, Франция
        (31.2357, 30.0444),  # Александрия, Египет
        (-33.8688, 151.2093),  # Сидней, Австралия
        (64.1265, -21.8174),  # Рейкьявик, Исландия (полярный круг)
        (78.2232, 15.6267)  # Лонгйир, Шпицберген (Арктика)
    ]

    for i, (lat, lon) in enumerate(test_cases, 1):
        # (i=1, (lat=40.7128, lon=-74.0060))
        response = await async_client.get(
            "/get-weather",
            params={"latitude": lat, "longitude": lon}
        )
        assert response.status_code == 200, f"Ошибка для координат ({lat}, {lon})"
        assert "айди" in response.json(), "Нет ключа 'айди' в ответе"
        assert isinstance(response.json()["айди"], str), "task_id должен быть строкой"
