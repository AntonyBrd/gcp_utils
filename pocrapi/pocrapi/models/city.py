from pydantic import BaseModel
from datetime import datetime

class City(BaseModel):
    name: str
    country: str | None = None
    lat: float | None = None
    lon: float | None = None
    population: int | None = None
    lastupdate: datetime