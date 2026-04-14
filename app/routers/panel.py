from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_club_role
from app.models.club import Club
from app.models.event import Event
from app.schemas.club import ClubOut
from app.schemas.event import EventCreate, EventOut, EventUpdate

router = APIRouter(prefix="/api/v1/panel", tags=["panel"])


# --- Me ---
@router.get("/me", response_model=ClubOut)
async def get_me(club: Club = Depends(require_club_role)):
    return club


# --- Events ---
@router.get("/events", response_model=list[EventOut])
async def list_my_events(
    club: Club = Depends(require_club_role), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Event).where(Event.club_id == club.id).order_by(Event.start_date.desc(), Event.start_time.desc())
    )
    return result.scalars().all()


@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(
    body: EventCreate,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    # Check max 2 events per month for this club
    event_month = body.start_date.month
    event_year = body.start_date.year
    count_result = await db.execute(
        select(func.count())
        .select_from(Event)
        .where(
            Event.club_id == club.id,
            extract("month", Event.start_date) == event_month,
            extract("year", Event.start_date) == event_year,
        )
    )
    count = count_result.scalar()
    if count >= 2:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Maximum 2 events per month for this club",
        )

    event = Event(
        title=body.title,
        description=body.description,
        event_type=body.event_type,
        start_date=body.start_date,
        start_time=body.start_time,
        end_date=body.end_date,
        end_time=body.end_time,
        audience=body.audience,
        mode=body.mode,
        language=body.language,
        address_name=body.address_name,
        address_street=body.address_street,
        address_city=body.address_city,
        room_number=body.room_number,
        status="pending",
        club_id=club.id,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.put("/events/{event_id}", response_model=EventOut)
async def update_event(
    event_id: int,
    body: EventUpdate,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Event).where(Event.id == event_id, Event.club_id == club.id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    event.status = "pending"

    await db.commit()
    await db.refresh(event)
    return event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Event).where(Event.id == event_id, Event.club_id == club.id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    await db.delete(event)
    await db.commit()
