from json import loads, dumps
from typing import Annotated

from fastapi import Depends

from app.backend.schemas import GeographicalCoordinates
from app.core import redis_cache

from app.services.geopy import fetch_data
from app.services.open_meteo import (
    get_humidity_status, get_pressure_status,
    get_wind_direction, get_location_name,
    get_weather_description, format_time
)


async def get_weather_data(user_data: Annotated[GeographicalCoordinates, Depends()]) -> dict[str, str]:
    redis = redis_cache
    cache_key = f"weather:{user_data.latitude}:{user_data.longitude}"

    cached_data = await redis.get(cache_key)
    if cached_data:
        result = loads(cached_data)
        # json.loads преобразует строку JSON в питон словарь, json.dumps - наоборот
        result["cached"] = True

        return result

    data = await fetch_data(data=user_data)

    current = data['current']
    daily = data['daily']
    hourly = data['hourly']

    # текущий час
    current_time = current['time']
    current_hour_index = hourly['time'].index(current_time[:13] + ':00')

    # доп статусы
    humidity_status = get_humidity_status(current['relative_humidity_2m'])
    pressure_status = get_pressure_status(current['pressure_msl'])
    wind_direction_deg = hourly['wind_direction_10m'][current_hour_index]
    wind_direction_text = get_wind_direction(wind_direction_deg)

    location_name = await get_location_name(data=user_data)

    weather_data = {
        "местоположение": {
            "название": location_name,
            "широта": f"{data['latitude']}° с.ш.",
            "долгота": f"{data['longitude']}° в.д.",
            "высота": f"{data['elevation']} м над уровнем моря",
            "часовой_пояс": data['timezone']
        },
        "температура": {
            "текущая": f"{current['temperature_2m']}°C",
            "ощущается_как": f"{current['apparent_temperature']}°C",
            "максимальная_сегодня": f"{daily['temperature_2m_max'][0]}°C",
            "минимальная_сегодня": f"{daily['temperature_2m_min'][0]}°C"
        },
        "ветер": {
            "скорость": f"{hourly['wind_speed_10m'][current_hour_index]} км/ч",
            "направление": f"{wind_direction_text} ({wind_direction_deg}°)",
            "порывы": f"{hourly['wind_gusts_10m'][current_hour_index]} км/ч"
        },
        "влажность": f"{current['relative_humidity_2m']}% - {humidity_status}",
        "давление": f"{current['pressure_msl']} гПа - {pressure_status}",
        "погодные_условия": get_weather_description(current['weather_code']),
        "время_солнца": {
            "восход": f"{format_time(daily['sunrise'][0])} по местному времени",
            "закат": f"{format_time(daily['sunset'][0])} по местному времени"
        }
    }

    await redis_cache.set(cache_key, dumps(weather_data), ex=600)
    weather_data["cached"] = False

    return weather_data
