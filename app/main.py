from fastapi import FastAPI
from app.routers import (
    reservation,
    service_site,
    queue_arranging,
    authentication,
    report,
)
from fastapi.middleware.cors import CORSMiddleware

description = """
Service Site API provides a vaccination queue for each user reservation
"""
tags_metadata = [
    {
        "name": "service site",
        "description": "Service site provides user a queue and vaccine",
    },
    {
        "name": "vaccine reservation",
        "description": "Vaccine reservation",
    },
    {"name": "authentication", "description": "jwt bearear token authentication"},
]

app = FastAPI(
    title="Service Site OGYH",
    description=description,
    version="1.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reservation.router, prefix="/api")
app.include_router(service_site.router, prefix="/api")
app.include_router(queue_arranging.router, prefix="/api")
app.include_router(authentication.router)
app.include_router(report.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    import requests

    res = requests.post(
        "https://wcg-apis-test.herokuapp.com/register_user",
        params={"username": "Chayapol", "password": "Kp6192649"},
    )
    print(res.status_code)


@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "hello from OGYH"}
