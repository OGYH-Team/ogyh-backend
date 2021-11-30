"""Api router for service site."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List

from app.utils.oauth2 import get_current_user
from app.utils.paginator import Paginator
from app.database import (
    add_site,
    delete_site,
    retrieve_site,
    retrive_sites,
    update_site,
)
from app.models.basic_model import Message
from app.models.service_site import Site
from app.models.user import User

router = APIRouter(tags=["service site"])


@router.get(
    "/sites",
    response_description="Service sites retrived",
    summary="Get every service sites",
    response_model=List[Site],
)
async def read_site_names(limit: Optional[int] = None, page: Optional[int] = 1):
    """
    ## Show service sites information:

    - **limit** : number of users to be shown as a result
    - **page** : number of pages to be shown as a result

    """
    sites = await retrive_sites()
    if sites:
        site_paginator = Paginator(sites)
        site_paginator.paginate(page=page, limit=limit)
        return site_paginator.get_items()
        # return {
        #     "response": {
        #         "page_data": site_paginator.get_page_data(),
        #         "service_sites": site_paginator.get_items()
        #     }
        # }


@router.get(
    "/site/{id}",
    response_description="Service site data retrived",
    summary="Get a service site info by id",
    response_model=Site,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message, "description": "Not found"},
    },
)
async def read_one_site(id: str):
    """
    ## Show a service site information:

    - **id** : service site id
    """
    site = await retrieve_site(id)
    if site:
        return Site(
            id =site["id"], name=site["name"], location=site["location"], capacity=site["capacity"]
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="service site is not found"
    )


@router.post(
    "/site",
    response_description="Service site data added into the database",
    summary="Create a new service site",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Create Successfull",
            "content": {
                "application/json": {
                    "example": {"response": "create site id site_id success"}
                }
            },
        }
    },
)
async def add_site_data(request: Site, current_user: User = Depends(get_current_user)):
    """
    ## Create a new service site:

    - **name** : service site name
    - **location** : service site location
    """
    result = dict(**request.dict())
    new_site = await add_site(result)
    return new_site


@router.put(
    "/site/{id}",
    response_description="Service site data updated into the database",
    summary="Update a service site",
    response_model=Message,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message, "description": "Not found"},
    },
)
async def updated_site(
    id: str, request: Site, current_user: User = Depends(get_current_user)
):
    """
    ## Update a service site information:

    - **id** : service site deleted id
    - **name** : a new service site name
    - **location** : a new service site location
    """
    new_value = dict(**request.dict())
    updated_site = await update_site(id, new_value)
    if updated_site:
        return Message(message=f"update {id} success")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"service site {id} not found"
    )


@router.delete(
    "/site/{id}",
    #    response_description="Service site data deleted from the database",
    summary="Remove a service site",
    response_model=Message,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message, "description": "Not found"},
    },
)
async def remove_site(id: str, current_user: User = Depends(get_current_user)):
    """
    ## Remove a service site information:

    - **id** : an id of service site deleted
    """
    deleted_site = await delete_site(id)
    if deleted_site:
        return Message(message=f"delete site id {id} success")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"service site {id} not found"
    )
