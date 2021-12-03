from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from app.database import db
from datetime import datetime, timedelta
from app.models.user import User
from app.models.time_slot import TimeSlots
from app.utils.oauth2 import get_current_user
from app.routers.reservation import read_users_reservations
from app.routers.service_site import read_one_site
from app.models.basic_model import Message
from bson.objectid import ObjectId
from typing import Optional, List
import requests
import bson

router = APIRouter(prefix="/site/{site_id}/queues", tags=["vaccine reservation"])

time_str = [
    "10:00-10:30",
    "10:30-11:00",
    "11:00-11:30",
    "11:30-12:00",
    "13:00-13:30",
    "13:30-14:00",
    "14:00-14:30",
    "14:30-15:00",
    "15:30-16:00",
]
time_format = "%Y/%m/%d"


@router.get("/", status_code=HTTP_200_OK, response_model=TimeSlots)
async def read_time_slots(site_id: str, date: Optional[str] = ""):
    """
    ## Retrive Vaccination Queue
    - **site_id**: a valid service provider site.
    - **date** : a specific time slot date time string.
    """
    try:
        service_site = await read_one_site(site_id)
    except bson.errors.InvalidId:
        message = f"Service site id {site_id} is invalid"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    all_time_slots = []
    async for time_slot in db.time_slots.find({"service_site": service_site.name}):
        all_time_slots.append({**time_slot, "_id": str(time_slot["_id"])})

    if len(all_time_slots) < 1:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Time slots in {site_id} is not found",
        )

    if date:
        selected_date = datetime.strptime(date, time_format)
        for time_slot in all_time_slots:
            if time_slot["date"] == selected_date:
                return time_slot
    return {"time_slots": all_time_slots}


@router.get("/update_queue", response_model=Message, status_code=HTTP_200_OK)
async def update_queue(site_id: str, current_user: User = Depends(get_current_user)):
    """
    ## Update Vaccination Queue
    - **site_id**: a valid service provider site.
    """
    # login for sending report
    res = requests.post(
        "https://wcg-apis-test.herokuapp.com/login", auth=("Chayapol", "Kp6192649")
    )
    access_token = res.json()["access_token"]

    reservations = (await read_users_reservations(site_id))["response"]["reservations"]

    try:
        service_site = await read_one_site(site_id)
    except bson.errors.InvalidId:
        message = f"Service site id {site_id} is invalid"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    # initialize time slot variables
    all_time_slots = []
    time_slot_index = 0
    time_str_index = 0
    delta_time = 5
    time_slot_size = service_site.capacity / len(time_str)
    current_date = datetime.today().strftime(time_format)
    date = datetime.strptime(current_date, time_format) + timedelta(days=delta_time)
    date_string = date.strftime(time_format)
    all_time_slots.append(
        {
            "service_site": service_site.name,
            "time_str": "10:00-10:30",
            "date": date_string,
            "reservations": [],
        }
    )
    count_reservation = 0

    # running through the reservations
    for reservation in reservations:
        if (reservation["checked"] == "True") or (reservation["queue"] != ""):
            continue
        if count_reservation == service_site.capacity:
            break
        if len(all_time_slots[time_slot_index]["reservations"]) == time_slot_size:
            time_str_index += 1
            queue = (date + timedelta(hours=10, minutes=30 * time_str_index)).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            if time_str_index == len(time_str):
                time_str_index = 0
                delta_time += 1

            reservation.update({"queue": queue})

            report = {
                "citizen_id": reservation["citizen_id"],
                "queue": reservation["queue"],
            }
            res = requests.post(
                "https://wcg-apis-test.herokuapp.com/queue_report",
                params=report,
                headers={"Authorization": "Bearer {}".format(access_token)},
            )
            all_time_slots.append(
                {
                    "service_site": service_site.name,
                    "time_str": time_str[time_str_index],
                    "date": (date + timedelta(days=delta_time)).strftime(time_format),
                    "reservations": [reservation],
                }
            )
            time_slot_index += 1

        else:
            queue = (date + timedelta(hours=10, minutes=30 * time_str_index)).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            reservation.update({"queue": queue})
            report = {
                "citizen_id": reservation["citizen_id"],
                "queue": reservation["queue"],
            }
            res = requests.post(
                "https://wcg-apis-test.herokuapp.com/queue_report",
                params=report,
                headers={"Authorization": "Bearer {}".format(access_token)},
            )

            all_time_slots[time_slot_index]["reservations"].append(reservation)
        count_reservation += 1
    try:
        async for time_slot in db.time_slots.find({"service_site": service_site.name}):
            if time_slot["date"] == date_string:
                await db.time_slots.delete_many(
                    {
                        "service_site": service_site.name,
                        "date": date_string,
                    }
                )
        for time_slot in all_time_slots:
            await db.time_slots.insert_one(time_slot)
        if count_reservation > service_site.capacity:
            return Message(message=f"service site id {site_id} is full on {date}")
    except:
        return Message(message="error occurred during queue updating")
    return Message(message="update queue successfully")


@router.delete("/{time_slot_id}", response_model=Message, status_code=HTTP_200_OK)
async def destroy_time_slot(
    site_id: str, time_slot_id: str, current_user: User = Depends(get_current_user)
):
    """
    ## Remove a vaccination time slot
    - **site_id**: a valid service provider site.
    - **time_slot_id**: a valid time slot id in the site_id.
    """
    time_slot = db.time_slots.find_one({"_id": ObjectId(time_slot_id)})
    if time_slot:
        await db.time_slots.delete_one({"_id": ObjectId(time_slot_id)})
        return Message(
            message=f"remove time slot id {time_slot_id} from site id {site_id} success"
        )
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f"time slot id {time_slot_id} not found"
    )


@router.get("/walkin", status_code=status.HTTP_200_OK)
async def read_walk_in(site_id: str):
    """
    ## Return a service site with its remaining capacity
    - **site_id**: a valid service provider site.
    """
    try:
        service_site = await read_one_site(site_id)
    except bson.errors.InvalidId:
        message = f"Service site id {site_id} is invalid"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    count = 0
    delta_time = 5
    current_date = datetime.today().strftime(time_format)
    date = datetime.strptime(current_date, time_format) + timedelta(days=delta_time)
    date_string = date.strftime(time_format)
    async for time_slot in db.time_slots.find({"service_site": service_site.name}):
        if time_slot["date"] == date_string:
            for reservation in time_slot["reservations"]:
                count += 1
    return {
        "response": {
            "service_site": service_site,
            "remaining": service_site.capacity - count
            if service_site.capacity > count
            else 0,
        }
    }
