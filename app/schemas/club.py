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
    logo_url: str | None = None
    type: str
    type_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    email: str | None = None
    facebook_url: str | None = None
    instagram_url: str | None = None
    website_url: str | None = None
    linkedin_url: str | None = None
    supervisor: str | None = None
    category: str | None = None
    category_en: str | None = None
    is_pinned: bool = False
    priority: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ClubDetailOut(ClubOut):
    events: list["EventOut"] = []


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    event_type: str | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: list[str] | None = None
    mode: str | None = None
    language: str | None = None
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
