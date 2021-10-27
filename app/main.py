
from fastapi import FastAPI
import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder

from app.utils.utils import arranging_reservation_by_site_name, fetch_url, get_cancellation
from app.utils.paginator import Paginator
from app.database import db
from app.models.site import Site

from app.routers import reservation, service_site

description = """
Service Site API provides a vaccination queue for each user reservation
"""
tags_metadata = [
    {
        "name": "service site",
        "description": "Service site provides user a queue and vaccine",
        "name": "reservation",
        "description": "Users reservation data and rules come from WCG group ",
        "externalDocs": {
            "description": "docs",
            "url": "https://wcg-apis.herokuapp.com/reservation_usage",
        },
    }
]

app = FastAPI(
    title="Service Site OGYH",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata,
)

app.include_router(reservation.router)
app.include_router(service_site.router)


@app.get("/", include_in_schema=False)
async def read_root():
    queue = await db.queue.find_one()
    all_sites = []
    async for site in db.sites.find({}, {"_id": 0}):
        all_sites.append(site)
    return {"msg": queue["msg"], "sites": all_sites}

