from fastapi.responses import ORJSONResponse
from uvicorn import run
from fastapi import FastAPI

from app.core import lifespan
from app.backend import get_weather_rout


app = FastAPI(
    title="Smart-Weather-Service",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
app.include_router(get_weather_rout)


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
