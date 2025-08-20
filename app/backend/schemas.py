from pydantic import BaseModel, confloat


latitude, longitude = (
    confloat(ge=-90.0, le=90.0),
    confloat(ge=-180.0, le=180.0)
)


class GeographicalCoordinates(BaseModel):
    latitude: float = latitude
    longitude: float = longitude
