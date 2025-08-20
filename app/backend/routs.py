from fastapi import APIRouter

from app.backend.schemas import GeographicalCoordinates
from app.core.lifespan import broker
from app.services import get_weather_data


get_weather_rout = APIRouter()


@broker.task
async def get_weather(user_input: GeographicalCoordinates):
    return await get_weather_data(user_data=user_input)


@get_weather_rout.get(path="/get-weather", status_code=200)
async def create_task(lat: float, lon: float):
    user_input = GeographicalCoordinates(latitude=lat, longitude=lon)
    task = await get_weather.kiq(user_input=user_input)
    result = await task.wait_result(timeout=7)

    return result.return_value
