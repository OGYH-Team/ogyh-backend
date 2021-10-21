from typing import Optional
from fastapi import FastAPI, HTTPException, Request

from .paginator import Paginator
from .utils import get_reservation, fetch_reservation, get_cancellation

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello from OGYH"}


@app.get("/reservations")
def read_users_reservations(
    request: Request,
    site_name: Optional[str] = "",
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information:

        - **request**:
        - **site_name** the vaccination site that provided vaccine to the user
        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result
    
    """  
    user_data = fetch_reservation(
        URL=request.url_for('sample_reservation_data'))
    user_data_by_site_name = get_reservation(user_data["data"])
    user_at_site = []
    site_names = user_data_by_site_name.keys()

    if site_name == "":
        site_name = "every sites"
        for user in user_data_by_site_name.values():
            user_at_site += user
    elif site_name not in site_names:
        raise HTTPException(status_code=404, detail="invalid site name")
    else:
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


@app.get("/sample-data")
def sample_reservation_data():
    DATA = [
        {"citizen_id": 1253567840123, "site_name": "site 1", "name": "nice"},
        {"citizen_id": 1234547890163, "site_name": "site 1", "name": "kaopun"},
        {"citizen_id": 1434567890123, "site_name": "site2", "name": "kuea"},
        {"citizen_id": 1234563890193, "site_name": "site2", "name": "tae"},
        {"citizen_id": 1234565890103, "site_name": "site-3", "name": "ice"},
        {"citizen_id": 1233547890183, "site_name": "site2", "name": "beam"},
        {"citizen_id": 1234567790173, "site_name": "site2", "name": "korn"},
        {"citizen_id": 1234378880133, "site_name": "site-3", "name": "thorn"},
    ]
    return {"data": DATA}


@app.get("/cancellation")
def users_cancellation(
    request: Request,
    citizen_id: Optional[int] = None,
):
    """
        Cancelled user vaccination information according to their citizen_id:

        - **request**: request from url
        - **citizen_id**: each cancellation must have a citizen_id 
    """
    user_data = fetch_reservation(
        URL=request.url_for('sample_reservation_data'))
    user_cancellation_data = get_cancellation(get_reservation(user_data["data"]), citizen_id)

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