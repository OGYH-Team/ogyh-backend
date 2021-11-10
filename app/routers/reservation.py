from fastapi import APIRouter, HTTPException
from typing import Optional
from fastapi.params import Body

from starlette import responses

from app.utils.utils import arranging_reservation_by_site_name, fetch_url, get_service_site_avaliable
from app.utils.paginator import Paginator
from app.database import retrieve_site

router = APIRouter(
    prefix="/site/{site_id}",
    tags=["reservation"]
)


@router.get("/reservations")
async def read_users_reservations(
    site_id: str,
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information:
        - **site_id** : a valid service site id
        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result
    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    site = await retrieve_site(site_id)

    if site:
        search_site = get_service_site_avaliable(
            data=user_data_by_site_name, key=site["name"])
        if search_site:
            user_data_at_site = user_data_by_site_name[search_site]
            user_paginator = Paginator(user_data_at_site)
            user_paginator.paginate(page=page, limit=limit)
            return {
                "response": {
                    "reservations_page_data": user_paginator.get_page_data(),
                    "reservations": user_paginator.get_items()
                }
            }
    raise HTTPException(status_code=404)


@router.get("/reservation/{citizen_id}")
async def read_users_reservations_by_site_name(
    site_id: str,
    citizen_id: str,
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information according to site name:

        - **site_id** : a valid service site id
        - **citizen_id**: a specific citizen_id
        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    site = await retrieve_site(site_id)

    if site:
        search_site = get_service_site_avaliable(
            data=user_data_by_site_name, key=site["name"])
        if search_site:
            user_data_at_site = user_data_by_site_name[search_site]
            for user in user_data_at_site:
                if(user["citizen_id"] == citizen_id):
                    print(user)
                    return user
    raise HTTPException(status_code=404, detail="site name is not found")


@router.delete("/reservation/{citizen_id}")
async def users_cancellation(
    site_id: str,
    citizen_id: str
):
    """
        Cancelled user vaccination information according to their citizen_id:

        - **site_id** : a valid service site id
        - **citizen_id**: each cancellation must have a citizen_id

    """
    import requests
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    site = await retrieve_site(site_id)
    if site:
        search_site = get_service_site_avaliable(
            data=user_data_by_site_name, key=site["name"])
        if search_site:
            user_data_at_site = user_data_by_site_name[search_site]
            for user in user_data_at_site:
                if(user["citizen_id"] == citizen_id):
                    body = {"citizen_id": citizen_id}
                    response = requests.delete("https://wcg-apis.herokuapp.com/reservations", data=body)
                    return user
    raise HTTPException(status_code=404, detail="citizen id not found")


@router.put("/reservation/{citizen_id}")
async def update_reservation(
    site_id: str,
    citizen_id: str,
):
    """
        Update user vaccination information according to their citizen_id:

        - **site_id** : a valid service site id
        - **citizen_id**: each cancellation must have a citizen_id

    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    site = await retrieve_site(site_id)
    if site:
        search_site = get_service_site_avaliable(
            data=user_data_by_site_name, key=site["name"])
        if search_site:
            user_data_at_site = user_data_by_site_name[search_site]
            for user in user_data_at_site:
                if(user["citizen_id"] == citizen_id):
                    # TODO update reservation
                    return user
    raise HTTPException(status_code=404, detail="citizen id not found")
