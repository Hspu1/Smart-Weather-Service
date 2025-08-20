from datetime import datetime


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_wind_direction(degrees):
    directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    index = round(degrees / 45) % 8

    return directions[index]


def get_weather_description(code):
    weather_codes = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Изморозь",
        51: "Лекая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        80: "Ливень",
        95: "Гроза"
    }
    return weather_codes[code]


def get_humidity_status(humidity):
    match humidity:
        case _ if humidity < 30:
            return "сухой воздух (норма: 40-60%)"
        case _ if 30 <= humidity <= 60:
            return "комфортная влажность (норма: 40-60%)"
        case _ if 61 <= humidity <= 70:
            return "повышенная влажность (норма: 40-60%)"

        case _:
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
