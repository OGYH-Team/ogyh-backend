from fastapi import APIRouter, HTTPException
from typing import Optional

from app.utils.utils import arranging_reservation_by_site_name, fetch_url, get_cancellation
from app.utils.paginator import Paginator

router = APIRouter(
    prefix="/site/{site_id}",
    tags=["reservation"]
)


@router.get("/reservations")
def read_users_reservations(
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information:

        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result
    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservation")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    user_at_site = []
    site_names = user_data_by_site_name.keys()
    for site_name in site_names:
        user_at_site += user_data_by_site_name[site_name]
    user_paginator = Paginator(user_at_site)
    user_paginator.paginate(page=page, limit=limit)

    return {
        "response": {
            "users_page_data": user_paginator.get_page_data(),
            "users": user_paginator.get_items()
        }
    }


@router.get("/reservation/{reservation_id}")
def read_users_reservations_by_site_name(
    reservation_id: int,
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information according to site name:

        - **site_name** : the vaccination site that provided vaccine to the user
        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservation")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    user_at_site = []
    # site_names = user_data_by_site_name.keys()

    # if site_name not in site_names:
    #     raise HTTPException(status_code=404, detail="site name is not found")
    # else:
    #     user_at_site = user_data_by_site_name[site_name]

    site_name = ""

    user_paginator = Paginator(user_at_site)
    user_paginator.paginate(page=page, limit=limit)

    return {
        "response": {
            "site_name": site_name,
            "users_page_data": user_paginator.get_page_data(),
            "users": user_paginator.get_items()
        }
    }


@router.delete("/reservation")
def users_cancellation(
    citizen_id: Optional[int] = None,
):
    """
        Cancelled user vaccination information according to their citizen_id:

        - **citizen_id**: each cancellation must have a citizen_id

    """
    user_data = {}
    user_cancellation_data = get_cancellation(
        arranging_reservation_by_site_name(user_data["data"]), citizen_id)

    if not citizen_id:
        raise HTTPException(status_code=404, detail="citizen id not provided")
    if not user_cancellation_data:
        raise HTTPException(status_code=404, detail="citizen id not found")

    return {
        "response": {
            "citizen_id": citizen_id,
            "site_name": user_cancellation_data['site_name'],
        }
    }


@router.patch("/reservation")
def update_reservation(
    citizen_id: Optional[int] = None,
):
    """
        Update user vaccination information according to their citizen_id:

        - **citizen_id**: each cancellation must have a citizen_id

    """
    update_data = {}

    return{
        "response": {
            "user": update_data
        }
    }
