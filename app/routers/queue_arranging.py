from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from app.database import db
from datetime import datetime, timedelta
from app.models.user import User
from app.utils.oauth2 import get_current_user
from app.routers.reservation import read_users_reservations
from app.routers.service_site import read_one_site
from app.models.basic_model import Message
from bson.objectid import ObjectId
from typing import Optional

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


@router.get("/")
async def read_time_slots(site_id: str, date: Optional[str] = ""):
    """
    ## Retrive Vaccination Queue
    - **site_id**: a valid service provider site.
    - **date** : a specific time slot date time string.
    """
    service_site = await read_one_site(site_id)
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


@router.get("/update_queue", response_model=Message)
async def update_queue(site_id: str, current_user: User = Depends(get_current_user)):
    """
    ## Update Vaccination Queue
    - **site_id**: a valid service provider site.
    """

    reservations = (await read_users_reservations(site_id))["response"]["reservations"]
    service_site = await read_one_site(site_id)
    all_time_slots = []
    time_slot_index = 0
    time_str_index = 0
    delta_time = 0
    time_slot_size = 10
    date = datetime.strptime("2021/11/20", time_format)
    all_time_slots.append(
        {
            "service_site": service_site.name,
            "time_str": "10:00-10:30",
            "date": "2021/11/20",
            "reservations": [],
        }
    )
    count_reservation = 0
    for reservation in reservations:
        if count_reservation == service_site.capacity:
            break
        if len(all_time_slots[time_slot_index]["reservations"]) == time_slot_size:
            queue = (date + timedelta(hours=10, minutes=30)).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            reservation.update({"queue": queue})
            time_str_index += 1
            if time_str_index == len(time_str):
                time_str_index = 0
                delta_time += 1
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
            all_time_slots[time_slot_index]["reservations"].append(reservation)
        count_reservation += 1
    try:
        async for time_slot in db.time_slots.find({"service_site": service_site.name}):
            if datetime.strptime(time_slot["date"], time_format) == date:
                await db.time_slots.delete_many(
                    {
                        "service_site": service_site.name,
                        "date": (date + timedelta(days=delta_time)).strftime(
                            time_format
                        ),
                    }
                )
        for time_slot in all_time_slots:
            await db.time_slots.insert_one(time_slot)
        if count_reservation > service_site.capacity:
            return Message(message=f"service site id {site_id} is full on {date}")
    except:
        return Message(message="error occurred during queue updating")
    return Message(message="update queue successfully")


@router.delete("/{time_slot_id}", response_model=Message)
async def destroy_time_slot(
    site_id: str, time_slot_id: str, current_user: User = Depends(get_current_user)
):
    time_slot = db.time_slots.find_one({"_id": ObjectId(time_slot_id)})
    if time_slot:
        await db.time_slots.delete_one({"_id": ObjectId(time_slot_id)})
        return Message(
            message=f"remove time slot id {time_slot_id} from site id {site_id} success"
        )
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f"time slot id {time_slot_id} not found"
    )


@router.get("/walkin")
async def read_walk_in(site_id: str):
    service_site = await read_one_site(site_id)
    count = 0
    async for time_slot in db.time_slots.find({"service_site": service_site.name}):
        total_reservation = len(time_slot["reservations"])
        count += total_reservation
    return {
        "response": {
            "service_site": service_site,
            "remaning": count - service_site.capacity,
        }
    }
