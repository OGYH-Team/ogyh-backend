from fastapi import APIRouter, Depends
from app.database import db
from datetime import datetime, timedelta
from app.utils.sample_reservations import sample_reservations
from app.models.user import User
from app.utils.oauth2 import get_current_user


router = APIRouter()

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
async def read_time_slots():
    all_time_slots = []
    async for time_slot in db.time_slots.find({}):
        all_time_slots.append({**time_slot, "_id": str(time_slot["_id"])})
    return {"time_slots": all_time_slots}


@router.get("/update_queue")
async def update_queue(current_user: User = Depends(get_current_user)):
    reservations = sorted(
        sample_reservations,
        key=lambda r: (r["citizen_data"]["occupation"], r["timestamp"]),
    )

    all_time_slots = []
    time_slot_index = 0
    time_str_index = 0
    delta_time = 0
    date = datetime.strptime("2021/11/20", time_format)

    all_time_slots.append(
        {"time_str": "10:00-10:30", "date": "2021/11/20", "reservations": []}
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
        return {"msg": "error occurred during queue updating"}

    return {"msg": "update queue successfully"}
