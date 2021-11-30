from pydantic import BaseModel, Extra
from app.models.reservation import Reservation
from typing import List


class TimeSlot(BaseModel):
    time_str: str
    date: str
    reservations: List[Reservation] = []

    class Config:
        extra = Extra.allow

class CitizenToReport(BaseModel):
    citizen_ids: List