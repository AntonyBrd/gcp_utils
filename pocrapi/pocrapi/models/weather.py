from pydantic import BaseModel
from datetime import datetime
class WeatherForcast(BaseModel):
    weather: str
    description: str | None = None
    icon: str | None = None
    date_time: datetime | None = None
    temperature: float | None = None
    humidity: float | None = None
    feels_like: float | None = None
    wind_speed: float | None = None
    lastupdate: datetime