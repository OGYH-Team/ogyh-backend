from pydantic import BaseModel, Extra


class Site(BaseModel):
    name: str
    location: str

    class Config:
        extra = Extra.allow
