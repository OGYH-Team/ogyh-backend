"""Api router for service site."""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.utils.paginator import Paginator
from app.database import add_site, delete_site, retrieve_site, retrived_sites, update_site
from app.models.site import Site

router = APIRouter(
    tags=["service site"]
)


@router.get("/sites", response_description="Service sites retrived")
async def read_site_names(
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show service sites information:

        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    sites = await retrived_sites()
    if sites:
        site_paginator = Paginator(sites)
        site_paginator.paginate(page=page, limit=limit)

        return {
            "response": {
                "service site data": site_paginator.get_page_data(),
                "service sites": site_paginator.get_items()
            }
        }


@router.get("/site/{id}", response_description="Service site data retrived")
async def read_one_site(
    id: str
):
    """
        Show a service site information:

        - **site_id** : service site id
    """
    site = await retrieve_site(id)
    if site:
        return {
            "response": {
                "message": "found a service site",
                "service site": {
                    "name": site["name"],
                    "location": site["location"]
                }
            }
        }
    raise HTTPException(
        status_code=404, detail="service site is not found")


@router.post("/site", response_description="Service site data added into the database", status_code=201)
async def add_site_data(
    name: str,
    location: str
):
    """
        Create a new service site:

        - **name** : service site name
        - **location** : service site location
    """
    site = {"name": name, "location": location}
    new_site = await add_site(site)
    return {
        "response": {
            "message": "create site successfully.",
        }
    }


@router.put("/site/{id}")
async def updated_site(
    id: str,
    name: Optional[str] = "",
    location: Optional[str] = "",
):
    """
        Update a service site information:

        - **site_id** : service site deleted id
        - **site_name** : service site name
        - **new_name** : a new service site name
        - **new_location** : a new service site location
    """

    new_value = {
        "name": name,
        "location": location
    }
    if not name:
        new_value.pop("name")
    if not location:
        new_value.pop("location")

    updated_site = await update_site(id, new_value)
    if updated_site:
        return{
            "response": {
                "message": f"update {id} success"
            }
        }
    raise HTTPException(
        status_code=404, detail=f"service site {id} not found")


@router.delete("/site/{id}", response_description="Service site data deleted from the database")
async def remove_site(
    id: str
):
    """
        Remove a service site information:

        - **site_name** : service site deleted name
    """
    deleted_site = await delete_site(id)
    if deleted_site:
        return {
            "response": {
                "message": f"delete success"
            }
        }
    raise HTTPException(
        status_code=404, detail=f"service site {id} not found")
