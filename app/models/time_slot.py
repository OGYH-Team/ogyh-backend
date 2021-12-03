from pydantic import BaseModel, Extra
from app.models.reservation import Reservation
from typing import List


class TimeSlot(BaseModel):
    _id: str
    service_site: str
    time_str: str
    date: str
    reservations: List[Reservation] = []

    class Config:
        extra = Extra.allow


class TimeSlots(BaseModel):
    time_slots: List[TimeSlot]


class CitizenToReport(BaseModel):
    citizen_ids: List


class Walkin(BaseModel):
    citizen_id: str
    vaccine_name: str
