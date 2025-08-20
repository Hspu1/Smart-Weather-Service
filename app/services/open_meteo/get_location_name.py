from asyncio import to_thread
from typing import Annotated

from fastapi import Depends
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from app.backend import GeographicalCoordinates


async def get_location_name(data: Annotated[GeographicalCoordinates, Depends()]) -> str:
    geolocator = Nominatim(user_agent="Smart-Weather-Service")
    try:
        location = await to_thread(geolocator.reverse, (data.latitude, data.longitude), exactly_one=True)
        if location:
            address = location.raw.get("address", {})

            return (
                    address.get("city") or address.get("town")
                    or address.get("village") or address.get("county")
                    or address.get("state") or address.get("country")
            )

        return (
            "Неизвестное место "
            "(не является официально признанным "
            "городом/деревней/округом/штатом/страной)"
        )

    except (GeocoderTimedOut, GeocoderServiceError):
        return "Ошибка геокодирования"
