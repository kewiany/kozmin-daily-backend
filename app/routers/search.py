from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.event import Event
from app.models.initiative import Initiative
from app.schemas.event import EventOut
from app.schemas.initiative import InitiativeOut

router = APIRouter(prefix="/api/v1/search", tags=["search"])


class SearchResponse(BaseModel):
    events: list[EventOut]
    initiatives: list[InitiativeOut]


@router.get("", response_model=SearchResponse)
async def search(
    q: str = "",
    audience: str | None = None,
    event_type: str | None = None,
    language: str | None = None,
    skip: int = 0,
    limit: int = Query(default=30, le=100),
    db: AsyncSession = Depends(get_db),
):
    # --- Events ---
    event_query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved")
    )
    if len(q) >= 3:
        pattern = f"%{q}%"
        event_query = event_query.where(
            Event.title.ilike(pattern) | Event.description.ilike(pattern)
        )
    if audience:
        event_query = event_query.where(Event.audience == audience)
    if event_type:
        event_query = event_query.where(Event.event_type == event_type)
    if language:
        event_query = event_query.where(Event.language == language)

    event_query = (
        event_query.order_by(Event.start_date.desc(), Event.start_time.desc())
        .offset(skip)
        .limit(limit)
    )
    event_result = await db.execute(event_query)
    events = event_result.scalars().all()

    # --- Initiatives ---
    init_query = (
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.status == "approved")
    )
    if len(q) >= 3:
        pattern = f"%{q}%"
        init_query = init_query.where(
            Initiative.title.ilike(pattern) | Initiative.description.ilike(pattern)
        )
    if audience:
        init_query = init_query.where(Initiative.audience == audience)
    if event_type:
        init_query = init_query.where(Initiative.event_type == event_type)
    if language:
        init_query = init_query.where(Initiative.language == language)

    init_query = (
        init_query.order_by(Initiative.start_date.desc(), Initiative.start_time.desc())
        .offset(skip)
        .limit(limit)
    )
    init_result = await db.execute(init_query)
    initiatives = init_result.scalars().all()

    return SearchResponse(events=events, initiatives=initiatives)
