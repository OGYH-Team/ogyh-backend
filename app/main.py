
from fastapi import FastAPI

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

app.include_router(reservation.router, prefix="/api")
app.include_router(service_site.router, prefix="/api")


@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "hello from OGYH"}
