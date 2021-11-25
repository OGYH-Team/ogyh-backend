from os import lstat
from typing import List, Dict, Optional
from pydantic import BaseModel, Extra, create_model


class Coordinates(BaseModel):
    lat: float
    lng: float


class Location(BaseModel):
    name: str
    address: str
    subdistrict: str
    province: str
    hours: str
    coordinates: Coordinates


class Site(BaseModel):
    name: str
    location: Location

    class Config:
        extra = Extra.allow


class Sites(BaseModel):
    service_sites: List[Site]

    class Config:
        extra = Extra.allow


class PageData(BaseModel):
    page_data = Dict[str, int]

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True


class GetSitesResponse(BaseModel):
    response: List[Site]


class GetSiteResponse(BaseModel):
    response: Site
