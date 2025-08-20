from typing import Annotated, Any

from fastapi import Depends, HTTPException
from httpx import AsyncClient, RequestError, HTTPStatusError

from app.backend import GeographicalCoordinates
from app.services.open_meteo import OPEN_METEO_URL


async def fetch_data(data: Annotated[GeographicalCoordinates, Depends()]) -> dict[str, Any]:
    params = {
        "latitude": data.lat,
        "longitude": data.lon,
        "current": "temperature_2m,apparent_temperature,weather_code,relative_humidity_2m,pressure_msl",
        "hourly": "wind_speed_10m,wind_direction_10m,wind_gusts_10m",
        "daily": "sunrise,sunset,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 1,
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "timeformat": "iso8601"
    }

    try:
        async with AsyncClient(timeout=30.0) as client:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            return response.json()

    except RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ошибка подключения к Open-Meteo: {str(e)}"
        )

    except HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Open-Meteo вернул ошибку: {e.response.status_code}"
        )
