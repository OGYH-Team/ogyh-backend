from typing import Dict, List
from pydantic import BaseModel, Extra


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


example_reservation = {
    "citizen_id": "1103403134124",
    "site_name": "og",
    "vaccine_name": "Astra",
    "timestamp": "2021-11-16 15:27:37.302545",
    "queue": "None",
    "checked": "False",
    "citizen_data": {
        "citizen_id": "1103403134124",
        "name": "Chayapol",
        "surname": "Chaipongsawalee",
        "birth_date": "2000-11-05",
        "occupation": "student",
        "phone_number": "0816192649",
        "is_risk": "False",
        "address": "bkk",
        "vaccine_taken": "[]",
    },
}

example_get_reservations = {"response": {
    "reservations": [example_reservation]}}

example_get_reservation = {"reservation": example_reservation}
