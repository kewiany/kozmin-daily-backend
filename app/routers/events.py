from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventOut

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("", response_model=list[EventOut])
async def list_events(
    skip: int = 0,
    limit: int = 20,
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved")
    )
    if event_type:
        query = query.where(Event.event_type == event_type)
    query = query.order_by(Event.start_date.desc(), Event.start_time.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/all", response_model=list[EventOut])
async def list_all_events(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved")
    )
    if date_from:
        query = query.where(Event.start_date >= date_from)
    if date_to:
        query = query.where(Event.start_date <= date_to)
    if event_type:
        query = query.where(Event.event_type == event_type)
    query = query.order_by(Event.start_date.asc(), Event.start_time.asc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/upcoming", response_model=list[EventOut])
async def list_upcoming_events(
    skip: int = 0,
    limit: int = 20,
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved", Event.start_date >= date.today())
    )
    if event_type:
        query = query.where(Event.event_type == event_type)
    query = query.order_by(Event.start_date.asc(), Event.start_time.asc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/past", response_model=list[EventOut])
async def list_past_events(
    skip: int = 0,
    limit: int = 20,
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.status == "approved", Event.start_date < date.today())
    )
    if event_type:
        query = query.where(Event.event_type == event_type)
    query = query.order_by(Event.start_date.desc(), Event.start_time.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Event)
        .options(selectinload(Event.club))
        .where(Event.id == event_id, Event.status == "approved")
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event
