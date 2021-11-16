from typing import Dict, List
from pydantic import BaseModel, Extra
from starlette import responses


class Reservation(BaseModel):
    citizen_id: str
    site_name: str
    vaccine_name: str
    timestamp: str
    queue: str
    checked: str
    citizen_data: Dict

class GetReservation(BaseModel):
    reservation: Reservation

    class Config:
        extra = Extra.allow

class GetReservations(BaseModel):
    reservations: List[Reservation] = []

    class Config:
        extra = Extra.allow

class GetReservationResponse(BaseModel):
    response: GetReservation

    class Config:
        extra = Extra.allow

class GetReservationsResponse(BaseModel):
    response: GetReservations

    class Config:
        extra = Extra.allow

class Message(BaseModel):
    message: str