from datetime import datetime

from pydantic import BaseModel


class InitiativeCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    date: datetime


class InitiativeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    date: datetime | None = None


class InitiativeOut(BaseModel):
    id: int
    title: str
    description: str | None
    category: str | None
    date: datetime
    status: str
    club_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
