"""Api router for service site."""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.utils.paginator import Paginator
from app.database import add_site, delete_site, retrieve_site, retrive_sites, update_site
from app.models.site import Site, GetSitesResponse, Message, GetSiteResponse

router = APIRouter(
    tags=["service site"]
)


@router.get("/sites",
            response_description="Service sites retrived",
            summary="Get every service sites",
            response_model=GetSitesResponse,
            responses={
                404: {"model": Message, "description": "Not found"},
                200: {"description": "Found a service site",
                      "content": {
                          "application/json": {
                              "example": {"response": [{"name": "service site 1", "location": "service site 1's location"}, {"name": "service site 2", "location": "service site 2's location"}, {"name": "service site 3", "location": "service site 3's location"}]}
                          }
                      }}
            }
            )
async def read_site_names(
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        ## Show service sites information:

        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    sites = await retrive_sites()
    if sites:
        site_paginator = Paginator(sites)
        site_paginator.paginate(page=page, limit=limit)

        return{
            "response": site_paginator.get_items()
        }
        # return {
        #     "response": {
        #         "page_data": site_paginator.get_page_data(),
        #         "service_sites": site_paginator.get_items()
        #     }
        # }


@router.get("/site/{id}",
            response_description="Service site data retrived",
            summary="Get a service site info by id",
            response_model=GetSiteResponse,
            responses={
                404: {"model": Message, "description": "Not found"},
                200: {"description": "Found a service site",
                      "content": {
                          "application/json": {
                              "example": {"response": {"name": "service site", "location": "location"}}
                          }
                      }}
            }
            )
async def read_one_site(
    id: str
):
    """
        ## Show a service site information:

        - **id** : service site id
    """
    site = await retrieve_site(id)
    if site:
        return {
            "response": {
                "name": site["name"],
                "location": site["location"]
            }
        }
    raise HTTPException(
        status_code=404, detail="service site is not found")


@router.post("/site",
             response_description="Service site data added into the database",
             summary="Create a new service site",
             status_code=201,
             response_model=Message,
             responses={
                 201: {"description": "Create Successfull",
                                      "content": {
                                          "application/json": {
                                              "example": {"response": "create site id site_id success"}
                                          }
                                      }}
             }
             )
async def add_site_data(
    site: Site,
):
    """
        ## Create a new service site:

        - **name** : service site name
        - **location** : service site location
    """
    result = dict(**site.dict())
    new_site = await add_site(result)
    return {
        "message": new_site
    }


@router.put("/site/{id}",
            response_description="Service site data updated into the database",
            summary="Update a service site",
            response_model=Message,
            responses={
                404: {"model": Message, "description": "Not found"},
                200: {"description": "Update Successfull",
                      "content": {
                          "application/json": {
                              "example": {"response": "update id site_id success"}
                          }
                      }}
            }
            )
async def updated_site(
    id: str,
    site: Site,
):
    """
        ## Update a service site information:

        - **id** : service site deleted id
        - **name** : a new service site name
        - **location** : a new service site location
    """
    new_value = dict(**site.dict())
    updated_site = await update_site(id, new_value)
    if updated_site:
        return{
            "message": f"update {id} success"
        }
    raise HTTPException(
        status_code=404, detail=f"service site {id} not found")


@router.delete("/site/{id}",
               #    response_description="Service site data deleted from the database",
               summary="Remove a service site",
               response_model=Message,
               responses={
                   404: {"model": Message, "description": "Not found"},
                   200: {"description": "Remove Successfull",
                         "content": {
                             "application/json": {
                                 "example": {"response": "delete site id site_id success"}
                             }
                         }}
               }
               )
async def remove_site(
    id: str
):
    """
        ## Remove a service site information:

        - **id** : an id of service site deleted
    """
    deleted_site = await delete_site(id)
    if deleted_site:
        return {
            "message": f"delete site id {id} success"
        }
    raise HTTPException(
        status_code=404, detail=f"service site {id} not found")
