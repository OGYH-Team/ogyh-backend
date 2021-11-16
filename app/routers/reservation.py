from fastapi import APIRouter, HTTPException
from typing import Optional
from fastapi.params import Body

from app.utils.utils import arranging_reservation_by_site_name, fetch_url, get_service_site_avaliable
from app.utils.paginator import Paginator
from app.database import retrieve_site
from app.models.reservation import GetReservationsResponse, GetReservationResponse, Message

router = APIRouter(
    prefix="/site/{site_id}",
    tags=["reservation"]
)


@router.get("/reservations",
            response_description="Reservation retrived",
            summary="Get every reservations",
            response_model=GetReservationsResponse,
            responses={
                200: {"description": "Found a service site",
                      "content": {
                          "application/json": {
                              "example": {
                                  "response": {
                                      "reservations": [
                                          {
                                              "citizen_id": "1103403134124",
                                              "site_name": "og",
                                              "vaccine_name": "Astra",
                                              "timestamp": "2021-11-16 15:27:37.302545",
                                              "queue": "None",
                                              "checked": "False",
                                              "citizen_data": {
                                                  "citizen_id": "1103403134124",
                                                  "name": "Chayapol",
                                                  "surname": "Chaipongsawalee",
                                                  "birth_date": "2000-11-05",
                                                  "occupation": "student",
                                                  "phone_number": "0816192649",
                                                  "is_risk": "False",
                                                  "address": "bkk",
                                                  "vaccine_taken": "[]"
                                              }
                                          }
                                      ]
                                  }
                              }
                          }
                      }}
            }
            )
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
    if len(user_data) <= 0:
        return{
            "response": {
                "No reservation"
            }
        }

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
                    # "reservations_page_data": user_paginator.get_page_data(),
                    "reservations": user_paginator.get_items()
                }
            }
    raise HTTPException(status_code=404)


@router.get("/reservation/{citizen_id}",
            response_description="Reservations retrived",
            summary="Get a reservation by citizen_id",
            response_model=GetReservationResponse,
            responses={
                404: {"model": Message, "description": "Not found"},
                200: {"description": "Found a reservations",
                      "content": {
                          "application/json": {
                              "example": {
                                  "reservation":
                                  {
                                      "citizen_id": "1103403134124",
                                      "site_name": "og",
                                      "vaccine_name": "Astra",
                                      "timestamp": "2021-11-16 15:27:37.302545",
                                      "queue": "None",
                                      "checked": "False",
                                      "citizen_data": {
                                          "citizen_id": "1103403134124",
                                          "name": "Chayapol",
                                          "surname": "Chaipongsawalee",
                                          "birth_date": "2000-11-05",
                                          "occupation": "student",
                                          "phone_number": "0816192649",
                                          "is_risk": "False",
                                          "address": "bkk",
                                          "vaccine_taken": "[]"
                                      }
                                  }

                              }
                          }
                      }
                      }
            }
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
                    return {"response": {
                        "reservation": user
                    }}
    raise HTTPException(status_code=404, detail="site name is not found")


# @router.delete("/reservation/{citizen_id}")
# async def users_cancellation(
#     site_id: str,
#     citizen_id: str
# ):
#     """
#         Cancelled user vaccination information according to their citizen_id:

#         - **site_id** : a valid service site id
#         - **citizen_id**: each cancellation must have a citizen_id

#     """
#     import requests
#     user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
#     user_data_by_site_name = arranging_reservation_by_site_name(user_data)

#     site = await retrieve_site(site_id)
#     if site:
#         search_site = get_service_site_avaliable(
#             data=user_data_by_site_name, key=site["name"])
#         if search_site:
#             user_data_at_site = user_data_by_site_name[search_site]
#             for user in user_data_at_site:
#                 if(user["citizen_id"] == citizen_id):
#                     body = {"citizen_id": citizen_id}
#                     response = requests.delete(
#                         "https://wcg-apis.herokuapp.com/reservations", data=body)
#                     return user
#     raise HTTPException(status_code=404, detail="citizen id not found")


# @router.put("/reservation/{citizen_id}")
# async def update_reservation(
#     site_id: str,
#     citizen_id: str,
# ):
#     """
#         Update user vaccination information according to their citizen_id:

#         - **site_id** : a valid service site id
#         - **citizen_id**: each cancellation must have a citizen_id

#     """
#     user_data = fetch_url("https://wcg-apis.herokuapp.com/reservations")
#     user_data_by_site_name = arranging_reservation_by_site_name(user_data)

#     site = await retrieve_site(site_id)
#     if site:
#         search_site = get_service_site_avaliable(
#             data=user_data_by_site_name, key=site["name"])
#         if search_site:
#             user_data_at_site = user_data_by_site_name[search_site]
#             for user in user_data_at_site:
#                 if(user["citizen_id"] == citizen_id):
#                     # TODO update reservation
#                     return user
#     raise HTTPException(status_code=404, detail="citizen id not found")
