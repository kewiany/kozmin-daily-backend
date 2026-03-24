from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    date: datetime


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime | None = None


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    date: datetime
    status: str
    club_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
