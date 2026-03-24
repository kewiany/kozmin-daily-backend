from datetime import datetime

from pydantic import BaseModel


class ClubOut(BaseModel):
    id: int
    name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ClubDetailOut(ClubOut):
    events: list["EventOut"] = []
    initiatives: list["InitiativeOut"] = []


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    date: datetime
    status: str
    club_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


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


ClubDetailOut.model_rebuild()
