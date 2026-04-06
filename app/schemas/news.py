from datetime import datetime

from pydantic import BaseModel

from app.schemas.club import ClubBrief


class NewsCreate(BaseModel):
    title: str
    description: str


class NewsUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class NewsOut(BaseModel):
    id: int
    title: str
    description: str
    club_id: int
    club: ClubBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
