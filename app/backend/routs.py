from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.backend import GeographicalCoordinates
from app.core.lifespan import broker
from app.services import get_weather_data


get_weather_rout = APIRouter()


@broker.task(
    task_name="get-weather-data",
    labels={
        "retry": True, "max_retries": 5,
        "retry_backoff": True, "retry_backoff_delay": 1
        # задержка 0, 1, 2, 4, 8
    }
)
@get_weather_rout.get(path="/get-weather", status_code=200)
async def get_weather(user_input: Annotated[GeographicalCoordinates, Depends()], request: Request):
    return await get_weather_data(user_data=user_input, request=request)
