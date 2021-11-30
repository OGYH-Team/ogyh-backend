from fastapi import APIRouter, Depends
from app.database import db
from datetime import datetime, timedelta
from app.routers import service_site
from app.utils.sample_reservations import sample_reservations
from app.models.user import User
from app.utils.oauth2 import get_current_user
from app.routers.reservation import read_users_reservations
from app.routers.service_site import read_one_site
from app.models.basic_model import Message

router = APIRouter(prefix="/site/{site_id}")

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


@router.get("/time_slots")
async def read_time_slots(site_id: str):
    """
    ## Retrive Vaccination Queue
    """
    service_site = await read_one_site(site_id)
    all_time_slots = []
    async for time_slot in db.time_slots.find({"service_site": service_site["response"]["name"]}):
        all_time_slots.append({**time_slot, "_id": str(time_slot["_id"])})
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
    date = datetime.strptime("2021/11/20", time_format)
    all_time_slots.append(
        {
            "service_site": service_site["response"]["name"],
            "time_str": "10:00-10:30",
            "date": "2021/11/20",
            "reservations": []}
    )

    for reservation in reservations:
        if len(all_time_slots[time_slot_index]["reservations"]) == 10:
            time_str_index += 1
            if time_str_index == len(time_str):
                time_str_index = 0
                delta_time += 1

            all_time_slots.append(
                {
                    "time_str": time_str[time_str_index],
                    "date": (date + timedelta(days=delta_time)).strftime(time_format),
                    "reservations": [reservation],
                }
            )
            time_slot_index += 1

        else:
            all_time_slots[time_slot_index]["reservations"].append(reservation)

    try:
        await db.time_slots.delete_many({})
        for time_slot in all_time_slots:
            await db.time_slots.insert_one(time_slot)
    except:
        return Message(message="error occurred during queue updating")
    return Message(message="update queue successfully")
