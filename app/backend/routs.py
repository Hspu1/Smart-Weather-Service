from fastapi import APIRouter
from taskiq_redis.exceptions import ResultIsMissingError

from app.backend.schemas import GeographicalCoordinates
from app.core.lifespan import broker
from app.services import get_weather_data


get_weather_rout = APIRouter()


@broker.task
async def get_weather(user_input: GeographicalCoordinates):
    return await get_weather_data(user_data=user_input)


@get_weather_rout.get(path="/get-weather", status_code=200)
async def create_task(latitude: float, longitude: float):
    user_input = GeographicalCoordinates(latitude=latitude, longitude=longitude)
    task = await get_weather.kiq(user_input=user_input)

    return {
        "айди": task.task_id,
    }


@get_weather_rout.get(path="/task-result/{task_id}", status_code=200)
async def get_task_result(task_id: str) -> dict[str, str | dict]:
    try:
        result = await broker.result_backend.get_result(task_id=task_id)
        if result is None:
            return {"статус": "выполняется"}

        return {
            "статус": "успешно",
            "результат": result.return_value
        }

    except ResultIsMissingError:
        return {"статус": "неверный айди"}
