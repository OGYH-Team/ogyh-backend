from bson.objectid import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient as MotorClient,
)
import motor.motor_asyncio
import os
import asyncio

# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"], tls=True, tlsAllowInvalidCertificates=True)
client = MotorClient(
    os.environ["MONGODB_URL"], tls=True, tlsAllowInvalidCertificates=True
)
client.get_io_loop = asyncio.get_running_loop
db = client.ogyhDatabase

site_collection = db.get_collection("sites")
users_collection = db.get_collection("users")


def site_helper(site) -> dict:
    """Return a dict that contain extracted cursor object."""
    return {"id": str(site["_id"]), "name": site["name"], "location": site["location"], "capacity": site["capacity"]}


async def retrive_sites():
    """Retrieve all students present in the database."""
    sites = []
    async for site in site_collection.find():
        sites.append(site_helper(site))
    return sites


async def add_site(site_data: dict):
    """Add a new student into to the database."""
    sites = await retrive_sites()
    for site in sites:
        if site_data["name"] == site["name"]:
            id = str(site["id"])
            return f"There's a service site with id {id} in a database"
    site = await site_collection.insert_one(site_data)
    new_site = await site_collection.find_one({"_id": site.inserted_id})
    return site_helper(new_site)


async def retrieve_site(id: str) -> dict:
    """Retrieve a student with a matching ID."""
    site = await site_collection.find_one({"_id": ObjectId(id)})
    if site:
        return site_helper(site)


async def update_site(id: str, data: dict):
    """Update a site with a matching ID."""
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    site = await site_collection.find_one({"_id": ObjectId(id)})
    if site:
        updated_student = await site_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


async def delete_site(id: str):
    """Delete a site from the database."""
    site = await site_collection.find_one({"_id": ObjectId(id)})
    if site:
        await site_collection.delete_one({"_id": ObjectId(id)})
        return True


def user_helper(user):
    """Return a dict that contain extracted cursor object."""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
    }


async def retrieve_user(username: str):
    """Retrieve a user with a matching username."""
    user = await users_collection.find_one({"username": username})
    if user:
        return user_helper(user)


async def retrieve_password(username: str):
    """Retrieve a user with a matching password."""
    user = await users_collection.find_one({"username": username})
    if user:
        return user_helper(user)
