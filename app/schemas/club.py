import datetime as dt
from datetime import datetime

from pydantic import BaseModel


class ClubBrief(BaseModel):
    id: int
    name: str
    logo_url: str | None = None
    type: str

    model_config = {"from_attributes": True}


class ClubOut(BaseModel):
    id: int
    name: str
    role: str
    logo_url: str | None = None
    type: str
    description: str | None = None
    email: str | None = None
    facebook_url: str | None = None
    instagram_url: str | None = None
    website_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ClubDetailOut(ClubOut):
    events: list["EventOut"] = []
    initiatives: list["InitiativeOut"] = []


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    address_name: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    room_number: str | None = None
    is_highlighted: bool = False
    status: str
    club_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class InitiativeOut(BaseModel):
    id: int
    title: str
    description: str | None
    category: str | None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    address_name: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    room_number: str | None = None
    is_highlighted: bool = False
    status: str
    club_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


ClubDetailOut.model_rebuild()
