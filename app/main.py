from fastapi.responses import ORJSONResponse
from uvicorn import run
from fastapi import FastAPI


app = FastAPI(
    title="Weather Aggregator",
    default_response_class=ORJSONResponse
)


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
