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


@app.get(path="/get-message", status_code=200)
async def get_message() -> dict[str, str]:
    return {
        "message": "Hello World"
    }


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
