from typing import Optional
from fastapi import FastAPI, Request

from .paginator import Paginator
from .utils import get_reservation, fetch_reservation
import math

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/reservations")
def read_users_reservations():
    user_data = fetch_reservation(URL="http://localhost/sample-data")
    user_data = get_reservation(user_data["data"])
    return {"data": user_data}


@app.get("/reservations/{site_name}")
def read_users_reservations_in_site(
    site_name: str,
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    user_data = fetch_reservation(URL="http://localhost/sample-data")
    user_data_by_site_name = get_reservation(user_data["data"])
    try:
        site_names = user_data_by_site_name.keys()
        if site_name not in site_names:
            return {"response": "invalid site name"}
        user_at_site = user_data_by_site_name[site_name]

        user_paginator = Paginator(user_at_site)
        user_paginator.paginate(page=page, limit=limit)

        return {
            "response": {
                "site_name": site_name,
                "users_page_data": user_paginator.get_page_data(),
                "users": user_paginator.get_items()
            }
        }
    except NameError:
        return {"response": "please fetch first"}


@app.get("/sample-data")
def sample_reservation_data():
    DATA = [
        {"citizen_id": 1253567840123, "site_name": "1", "name": "nice"},
        {"citizen_id": 1234547890163, "site_name": "1", "name": "kaopun"},
        {"citizen_id": 1434567890123, "site_name": "2", "name": "kuea"},
        {"citizen_id": 1234563890193, "site_name": "2", "name": "tae"},
        {"citizen_id": 1234565890103, "site_name": "3", "name": "ice"},
        {"citizen_id": 1233547890183, "site_name": "2", "name": "beam"},
        {"citizen_id": 1234567790173, "site_name": "2", "name": "korn"},
        {"citizen_id": 1234378880133, "site_name": "3", "name": "thorn"},
    ]
    return {"data": DATA}
