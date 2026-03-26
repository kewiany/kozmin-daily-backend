import datetime as dt
from datetime import datetime

from pydantic import BaseModel

from app.schemas.club import ClubBrief


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    location: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: dt.date | None = None
    start_time: dt.time | None = None
    end_date: dt.date | None = None
    end_time: dt.time | None = None
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    location: str | None = None


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    location: str | None = None
    is_highlighted: bool = False
    status: str
    club_id: int
    club: ClubBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
