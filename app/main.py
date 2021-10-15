from typing import Optional
from fastapi import FastAPI, Request
from .utils import get_reservation, fetch_reservation

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/reservations")
def read_users_reservations():
    global user_data
    user_data = fetch_reservation(URL="http://localhost/sample-data")
    user_data = get_reservation(user_data["data"])
    return {"data": user_data}


@app.get("/reservations/{site_name}")
def read_users_reservations_in_site(site_name: str):
    try:
        site_names = user_data.keys()
        if site_name not in site_names:
            return {"response": "invalid site name"}
        user_at_site = user_data[site_name]

        return {"response": {
            "site_name": site_name,
            "many": len(user_at_site),
            "users": [user["citizen_id"] for user in user_at_site]}
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
