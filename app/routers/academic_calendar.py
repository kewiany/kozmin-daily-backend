from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.academic_calendar import AcademicCalendarEntry
from app.schemas.academic_calendar import AcademicCalendarEntryResponse

router = APIRouter(prefix="/api/v1/academic-calendar", tags=["academic-calendar"])


@router.get("", response_model=list[AcademicCalendarEntryResponse])
async def list_academic_calendar(
    year: str = Query(default="2025/2026"),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(AcademicCalendarEntry)
        .where(AcademicCalendarEntry.academic_year == year)
        .order_by(
            AcademicCalendarEntry.study_mode,
            AcademicCalendarEntry.semester,
            AcademicCalendarEntry.start_date,
        )
    )
    result = await db.execute(query)
    return result.scalars().all()
