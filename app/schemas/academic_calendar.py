import datetime as dt

from pydantic import BaseModel


class AcademicCalendarEntryResponse(BaseModel):
    id: int
    academic_year: str
    study_mode: str
    semester: str
    category: str
    title: str
    start_date: dt.date
    end_date: dt.date
    college: str | None = None

    model_config = {"from_attributes": True}


class AcademicCalendarResponse(BaseModel):
    entries: list[AcademicCalendarEntryResponse]
