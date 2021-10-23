from typing import Optional
from fastapi import FastAPI, HTTPException, Request

from app.utils.utils import arranging_reservation_by_site_name, fetch_url, get_cancellation
from app.utils.paginator import Paginator


description = """
Service Site API provides a vaccination queue for each user reservation
"""
tags_metadata = [
    {
        "name": "reservation",
        "description": "Users reservation data and rules come from WCG group ",
        "externalDocs": {
            "description": "docs",
            "url": "https://wcg-apis.herokuapp.com/reservation_usage",
        }
    }
]

app = FastAPI(
    title="Service Site OGYH",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata,
)


@app.get("/", include_in_schema=False)
def read_root():
    return {"msg": "Hello from OGYH"}


@app.get("/reservations", tags=["reservation"])
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


@app.get("/reservations/{site_name}", tags=["reservation"])
def read_users_reservations_by_site_name(
    site_name: str,
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show users vaccination reservations information:

        - **site_name** : the vaccination site that provided vaccine to the user
        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    user_data = fetch_url("https://wcg-apis.herokuapp.com/reservation")
    user_data_by_site_name = arranging_reservation_by_site_name(user_data)

    user_at_site = []
    site_names = user_data_by_site_name.keys()

    if site_name not in site_names:
        raise HTTPException(status_code=404, detail="site name is not found")
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


@app.delete("/reservation", tags=["reservation"])
def users_cancellation(
    request: Request,
    citizen_id: Optional[int] = None,
):
    """
        Cancelled user vaccination information according to their citizen_id:

        - **citizen_id**: each cancellation must have a citizen_id

    """
    user_data = fetch_url(
        URL=request.url_for('sample_reservation_data'))
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


@app.get("/sample-data", include_in_schema=False)
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
