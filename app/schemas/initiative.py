import datetime as dt
from datetime import datetime

from pydantic import BaseModel

from app.schemas.club import ClubBrief


class InitiativeCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None


class InitiativeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    start_date: dt.date | None = None
    start_time: dt.time | None = None
    end_date: dt.date | None = None
    end_time: dt.time | None = None
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None


class InitiativeOut(BaseModel):
    id: int
    title: str
    description: str | None
    category: str | None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: str | None = None
    event_type: str | None = None
    language: str | None = None
    status: str
    club_id: int
    club: ClubBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
