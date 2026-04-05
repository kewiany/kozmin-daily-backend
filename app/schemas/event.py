import datetime as dt
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from app.schemas.club import ClubBrief

VALID_CATEGORIES = [
    "Wydarzenie merytoryczne",
    "Targi",
    "Rekrutacja",
    "Integracja",
    "Wydarzenie sportowe",
]

CategoryType = Literal[
    "Wydarzenie merytoryczne",
    "Targi",
    "Rekrutacja",
    "Integracja",
    "Wydarzenie sportowe",
]


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    category: CategoryType | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    address_name: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    room_number: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: CategoryType | None = None
    start_date: dt.date | None = None
    start_time: dt.time | None = None
    end_date: dt.date | None = None
    end_time: dt.time | None = None
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    address_name: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    room_number: str | None = None


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    category: str | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    address_name: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    room_number: str | None = None
    is_highlighted: bool = False
    status: str
    club_id: int
    club: ClubBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
