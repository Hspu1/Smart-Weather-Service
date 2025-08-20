from fastapi.responses import ORJSONResponse
from uvicorn import run
from fastapi import FastAPI

from app.backend import GeographicalCoordinates
from app.core import lifespan
from app.core.lifespan import broker
from app.services import get_weather_data


app = FastAPI(
    title="Smart-Weather-Service",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@broker.task
async def get_weather(user_input: GeographicalCoordinates):
    return await get_weather_data(user_data=user_input)


@app.get(path="/get-weather", status_code=200)
async def create_task(lat: float, lon: float):
    user_input = GeographicalCoordinates(latitude=lat, longitude=lon)
    task = await get_weather.kiq(user_input=user_input)
    result = await task.wait_result(timeout=7)

    return result.return_value


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
