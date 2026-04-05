from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventOut

router = APIRouter(prefix="/api/v1/search", tags=["search"])


class SearchResponse(BaseModel):
    events: list[EventOut]


@router.get("", response_model=SearchResponse)
async def search(
    q: str = "",
    audience: str | None = None,
    event_type: str | None = None,
    mode: str | None = None,
    language: str | None = None,
    skip: int = 0,
    limit: int = Query(default=30, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved")
    )
    if len(q) >= 3:
        pattern = f"%{q}%"
        query = query.where(
            Event.title.ilike(pattern) | Event.description.ilike(pattern)
        )
    if audience:
        query = query.where(Event.audience.contains([audience]))
    if event_type:
        query = query.where(Event.event_type == event_type)
    if mode:
        query = query.where(Event.mode == mode)
    if language:
        query = query.where(Event.language == language)
    query = (
        query.order_by(Event.start_date.desc(), Event.start_time.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    events = result.scalars().all()

    return SearchResponse(events=events)
