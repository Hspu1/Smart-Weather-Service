from typing import Annotated

from fastapi import APIRouter, Depends

from app.backend import GeographicalCoordinates


get_weather_rout = APIRouter()


@get_weather_rout.get(path="/get-weather", status_code=200)
async def get_weather(user_input: Annotated[GeographicalCoordinates, Depends()]):
    ...
