from typing import List, Dict, Optional
from pydantic import BaseModel, Extra, create_model
from starlette import responses


class Site(BaseModel):
    name: str
    location: str

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


class Message(BaseModel):
    message: str
