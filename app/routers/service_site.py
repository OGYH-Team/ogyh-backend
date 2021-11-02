"""Api router for service site."""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.utils.paginator import Paginator
from app.database import db

router = APIRouter(
    tags=["service site"]
)


@router.get("/sites")
async def read_site_names(
    limit: Optional[int] = None,
    page: Optional[int] = 1
):
    """
        Show service sites information:

        - **limit** : number of users to be shown as a result
        - **page** : number of pages to be shown as a result

    """
    # TODO get all service site at db
    all_sites = []
    async for site in db.sites.find({}, {"_id": 0}):
        all_sites.append(site)

    site_paginator = Paginator(all_sites)
    site_paginator.paginate(page=page, limit=limit)

    return {
        "response": {
            "service site data": site_paginator.get_page_data(),
            "service sites": site_paginator.get_items()
        }
    }


@router.get("/site/{site_name}")
async def read_one_site(
    site_name: str
):
    """
        Show a service site information:

        - **site_id** : service site id
    """
    site = await db.sites.find_one({"name": site_name})
    if not site:
        raise HTTPException(
            status_code=404, detail="service site is not found")
    return {
        "response": {
            "message": "found a service site",
            "service site": {
                "name": site["name"],
                "location": site["location"]
            }
        }
    }


@router.post("/site")
async def create_site(
    name: str,
    location: str
):
    """
        Create a new service site:

        - **name** : service site name
        - **location** : service site location
    """
    
    async for site in db.sites.find({"name": name}):
        if site:
            return{
                "response":{
                    "message": "servide site is existed",
                    "service site": {
                        "name": site["name"],
                        "location": site["location"]
                    }
                }
            }
    await db.sites.insert_one({
        "name": name.capitalize(),
        "location": location
    })
    return {
        "response": {
            "message": "create site success",
        }
    }


@router.patch("/site/{site_name}")
async def update_site(
    site_name: str,
    new_name: Optional[str]="",
    new_location: Optional[str]="",
):
    """
        Update a service site information:

        - **site_id** : service site deleted id
        - **site_name** : service site name
        - **new_name** : a new service site name
        - **new_location** : a new service site location
    """
    new_value = {
        "$set": {
            "name": new_name,
            "location": new_location
        }
    }
    if not new_name:
        new_value["$set"].pop("name")
    if not new_location:
        new_value["$set"].pop("location")

    query = {"name": site_name}
    await db.sites.update_one(query, new_value)

    return{
        "response": {
            "message": "update success"
        }
    }


@router.delete("/site/{site_name}")
async def remove_site(
    site_name: str
):
    """
        Remove a service site information:

        - **site_name** : service site deleted name
    """

    await db.sites.delete_one({"name": site_name})
    return {
        "response": {
            "message": "remove success"
        }
    }

@router.delete("/sites")
async def remove_all_site():
    """
        Remove all service site 
    """
    delete_count = await db.sites.delete_many({}).delete_count
    return{
        "response": {
            "message": "remove success",
            "document deleted": delete_count
        }
    }
