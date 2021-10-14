from typing import Optional
from fastapi import FastAPI, Request
from .utils import get_reservation

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reservations")
def read_users_reservations():
    return {"data": get_reservation}


@app.get("/reservations/{site_name}")
def read_users_reservations_in_site(site_name: str):
    data = get_reservation()
    return {"data": data[site_name]}
