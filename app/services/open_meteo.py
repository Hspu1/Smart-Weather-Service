import asyncio
from datetime import datetime
from typing import Annotated, Dict, Any

from httpx import AsyncClient, RequestError, HTTPStatusError
from fastapi import Depends, HTTPException

from app.backend import GeographicalCoordinates


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


# async def fetch_data(data: Annotated[GeographicalCoordinates, Depends()]) -> Dict[str, Any]:
async def fetch_data(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        # Текущие данные: температура, ощущение, погода, влажность, давление
        "current": "temperature_2m,apparent_temperature,weather_code,relative_humidity_2m,pressure_msl",
        # Почасовые данные: ветер (скорость, направление, порывы)
        "hourly": "wind_speed_10m,wind_direction_10m,wind_gusts_10m",
        # Ежедневные данные: восход, закат, макс/мин температура
        "daily": "sunrise,sunset,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 1,  # Только сегодняшний прогноз
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "timeformat": "iso8601"
    }

    # 0: "Ясно",
    # 1: "Преимущественно ясно",
    # 2: "Переменная облачность",
    # 3: "Пасмурно",
    # 45: "Туман",
    # 48: "Изморозь",
    # 51: "Лекая морось",
    # 53: "Умеренная морось",
    # 55: "Сильная морось",
    # 61: "Небольшой дождь",
    # 63: "Умеренный дождь",
    # 65: "Сильный дождь",
    # 80: "Ливень",
    # 95: "Гроза"

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


async def main():
    data = await fetch_data(55.7558, 37.6176)
    return print(data)


if __name__ == '__main__':
    asyncio.run(main())


def get_wind_direction(degrees):
    directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    index = round(degrees / 45) % 8
    return directions[index]


def get_weather_description(code):
    weather_codes = {
        0: "Ясно ☀️",
        1: "Преимущественно ясно 🌤",
        2: "Переменная облачность ⛅",
        3: "Пасмурно ☁️",
        45: "Туман 🌫",
        48: "Изморозь 🌫",
        51: "Лекая морось 🌧",
        53: "Умеренная морось 🌧",
        55: "Сильная морось 🌧",
        61: "Небольшой дождь 🌧",
        63: "Умеренный дождь 🌧",
        65: "Сильный дождь 🌧",
        80: "Ливень ⛈",
        95: "Гроза ⛈"
    }
    return weather_codes[code]


def get_humidity_status(humidity):
    if humidity < 30:
        return "сухой воздух (норма: 40-60%)"
    elif 30 <= humidity <= 60:
        return "комфортная влажность (норма: 40-60%)"
    elif 61 <= humidity <= 70:
        return "повышенная влажность (норма: 40-60%)"
    else:
        return "высокая влажность (норма: 40-60%)"


def get_pressure_status(pressure):
    match pressure:
        case _ if pressure < 980:
            return "низкое давление (норма: 1013 гПа)"
        case _ if 980 <= pressure < 1000:
            return "пониженное давление (норма: 1013 гПа)"
        case _ if 1000 <= pressure <= 1026:
            return "нормальное давление (норма: 1013 гПа)"
        case _ if 1026 < pressure <= 1040:
            return "повышенное давление (норма: 1013 гПа)"

        case _:
            return "высокое давление (норма: 1013 гПа)"


def format_time(time_str):
    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    return dt.strftime("%H:%M")


async def get_weather_data(lat, lon):
    data = await fetch_data(lat, lon)

    current = data['current']
    daily = data['daily']
    hourly = data['hourly']

    # Получаем текущий час для актуальных данных о ветре
    current_time = current['time']
    current_hour_index = hourly['time'].index(current_time[:13] + ':00')

    # Получаем дополнительные статусы
    humidity_status = get_humidity_status(current['relative_humidity_2m'])
    pressure_status = get_pressure_status(current['pressure_msl'])
    wind_direction_deg = hourly['wind_direction_10m'][current_hour_index]
    wind_direction_text = get_wind_direction(wind_direction_deg)

    weather_data = {
        "местоположение": {
            "широта": f"{data['latitude']}° с.ш.",
            "долгота": f"{data['longitude']}° в.д.",
            "высота": f"{data['elevation']} м над уровнем моря",
            "часовой_пояс": data['timezone']
        },
        "время_данных": f"{format_time(current['time'])} (МСК)",
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
            "восход": f"{format_time(daily['sunrise'][0])} МСК",
            "закат": f"{format_time(daily['sunset'][0])} МСК"
        }
    }

    return weather_data
