"""Api router for reservation."""
from fastapi import APIRouter, HTTPException, status
from typing import Optional

from app.utils.utils import (
    arranging_reservation_by_site_name,
    fetch_url,
    get_service_site_avaliable,
    get_access_to_api
)
from app.utils.paginator import Paginator
from app.database import retrieve_site
from app.models.basic_model import Message
from app.models.reservation import (
    GetReservationsResponse,
    GetReservationResponse,
)
import bson
import requests

router = APIRouter(prefix="/site/{site_id}", tags=["vaccine reservation"])


@router.get(
    "/reservations",
    response_description="Reservation retrived",
    summary="Get every reservations",
    response_model=GetReservationsResponse,
)
async def read_users_reservations(
    site_id: str, limit: Optional[int] = None, page: Optional[int] = 1
):
    """
    Show users vaccination reservations information:
    - **site_id** : a valid service site id
    - **limit** : number of users to be shown as a result
    - **page** : number of pages to be shown as a result
    """
    user_data = fetch_url(
        "https://wcg-apis-test.herokuapp.com/reservations", token=get_access_to_api()
    )
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)
    try:
        site = await retrieve_site(site_id)
    except bson.errors.InvalidId:
        message = f"Service site id {site_id} is invalid"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    if site:
        try:
            name = site["name"]
            user_data_at_site = user_data_by_site_name[name]
            user_paginator = Paginator(user_data_at_site)
            user_paginator.paginate(page=page, limit=limit)
            return {
                "response": {
                    # "reservations_page_data": user_paginator.get_page_data(),
                    "reservations": user_paginator.get_items()
                }
            }
        except:
            message = f"Reservation in Service site {site_id} not found"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/reservation/{citizen_id}",
    response_description="Reservations retrived",
    summary="Get a reservation by citizen_id",
    response_model=GetReservationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message, "description": "Not found"},
    },
)
async def read_users_reservation(
    site_id: str,
    citizen_id: str,
):
    """
    Show users a vaccination reservation information according to citizen id:

    - **site_id** : a valid service site id
    - **citizen_id**: a specific citizen_id

    """
    user_data = fetch_url(
        "https://wcg-apis-test.herokuapp.com/reservations", token=get_access_to_api()
    )
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)
    try:
        site = await retrieve_site(site_id)
    except bson.errors.InvalidId:
        message = f"Service site id {site_id} is invalid"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    if site:
        search_site = get_service_site_avaliable(
            data=user_data_by_site_name, key=site["name"]
        )
        if search_site:
            user_data_at_site = user_data_by_site_name[search_site]
            for user in user_data_at_site:
                if user["citizen_id"] == citizen_id:
                    return {"response": {"reservation": user}}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="site name is not found"
    )
