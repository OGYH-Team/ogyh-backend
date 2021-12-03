from fastapi import APIRouter
from app.models.time_slot import CitizenToReport
from ..models.basic_model import Message
from .queue_arranging import read_time_slots
import requests

router = APIRouter(prefix="/site/{site_id}/queues", tags=["vaccine reservation"])


@router.post("/report")
async def send_report(request: CitizenToReport, site_id: str):
    """
    ## Create a queue report and send to government.
    - **site_id**: a valid service provider site.
    - *citizen_ids*: a valid list of citizen id to report.
    """
    res = requests.post(
        "https://wcg-apis-test.herokuapp.com/login", auth=("Chayapol", "Kp6192649")
    )
    access_token = res.json()["access_token"]
    time_slots = await read_time_slots(site_id)
    to_report_list = []
    for time_slot in time_slots["time_slots"]:
        for reservation in time_slot["reservations"]:
            if reservation["citizen_id"] in request.citizen_ids:
                to_report_list.append(reservation)
    for reservation in to_report_list:
        report = {
            "citizen_id": reservation["citizen_id"],
            "queue": reservation["queue"],
        }
        res = requests.post(
            "https://wcg-apis-test.herokuapp.com/queue_report",
            params=report,
            headers={"Authorization": "Bearer {}".format(access_token)},
        )

    return Message(message=f"report {len(to_report_list)} reservations success")


@router.post("/report-taken")
async def send_vaccinated_report(request: CitizenToReport, site_id: str):
    """
    ## Create a vaccine report and send to government.
    - **site_id**: a valid service provider site.
    - *citizen_ids*: a valid list of citizen id to report.
    """
    res = requests.post(
        "https://wcg-apis-test.herokuapp.com/login", auth=("Chayapol", "Kp6192649")
    )
    access_token = res.json()["access_token"]
    time_slots = await read_time_slots(site_id)
    to_report_list = []
    for time_slot in time_slots["time_slots"]:
        for reservation in time_slot["reservations"]:
            if reservation["citizen_id"] in request.citizen_ids:
                to_report_list.append(reservation)
    for reservation in to_report_list:
        report = {
            "citizen_id": reservation["citizen_id"],
            "vaccine_name": reservation["vaccine_name"],
            "option": "reserve",
        }
        res = requests.post(
            "https://wcg-apis-test.herokuapp.com/report_taken",
            params=report,
            headers={"Authorization": "Bearer {}".format(access_token)},
        )
    return Message(message=f"report {len(to_report_list)} reservations success")
