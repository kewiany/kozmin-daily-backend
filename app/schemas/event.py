import datetime as dt
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.schemas.club import ClubBrief

EventTypeKey = Literal["merit", "fair", "recruitment", "integration", "sport", "conference"]
AudienceKey = Literal["open", "students", "candidates", "alumni"]
ModeKey = Literal["online", "offline", "hybrid"]
LanguageKey = Literal["pl", "en"]


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=3000)
    event_type: EventTypeKey | None = None
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date
    end_time: dt.time
    audience: list[AudienceKey] | None = None
    mode: ModeKey | None = None
    language: LanguageKey | None = None
    address_name: str | None = Field(default=None, max_length=100)
    address_street: str | None = Field(default=None, max_length=100)
    address_city: str | None = Field(default=None, max_length=100)
    room_number: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self):
        today = dt.date.today()
        if self.start_date < today:
            raise ValueError("Data rozpoczęcia nie może być wcześniejsza niż dzisiaj")
        if self.end_date < self.start_date:
            raise ValueError("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia")
        if self.end_date == self.start_date and self.end_time < self.start_time:
            raise ValueError("Godzina zakończenia nie może być wcześniejsza niż godzina rozpoczęcia w tym samym dniu")
        return self


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=3000)
    event_type: EventTypeKey | None = None
    start_date: dt.date | None = None
    start_time: dt.time | None = None
    end_date: dt.date | None = None
    end_time: dt.time | None = None
    audience: list[AudienceKey] | None = None
    mode: ModeKey | None = None
    language: LanguageKey | None = None
    address_name: str | None = Field(default=None, max_length=100)
    address_street: str | None = Field(default=None, max_length=100)
    address_city: str | None = Field(default=None, max_length=100)
    room_number: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None and self.start_date < dt.date.today():
            raise ValueError("Data rozpoczęcia nie może być wcześniejsza niż dzisiaj")
        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia")
            if self.end_date == self.start_date and self.start_time is not None and self.end_time is not None:
                if self.end_time < self.start_time:
                    raise ValueError("Godzina zakończenia nie może być wcześniejsza niż godzina rozpoczęcia w tym samym dniu")
        return self


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
    club: ClubBrief | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
