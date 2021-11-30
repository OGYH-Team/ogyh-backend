from os import lstat
from typing import List, Dict, Optional
from pydantic import BaseModel, Extra, create_model

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class Location(BaseModel):
    formatted_address: str
    country: str
    postal: str
    route: str
    city: str
    coordinates: Coordinate

    class Config:
        extra = Extra.allow


class Site(BaseModel):
    name: str
    location: Location
    capacity: int

    class Config:
        extra = Extra.allow


class PageData(BaseModel):
    page_data = Dict[str, int]

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True


# class GetSitesResponse(BaseModel):
#     response: List[Site]


# class GetSiteResponse(BaseModel):
#     response: Site
