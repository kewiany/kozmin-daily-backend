from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_club_role
from app.models.club import Club
from app.models.event import Event
from app.models.initiative import Initiative
from app.schemas.club import ClubOut
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.schemas.initiative import InitiativeCreate, InitiativeOut, InitiativeUpdate

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
        start_date=body.start_date,
        start_time=body.start_time,
        end_date=body.end_date,
        end_time=body.end_time,
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


# --- Initiatives ---
@router.get("/initiatives", response_model=list[InitiativeOut])
async def list_my_initiatives(
    club: Club = Depends(require_club_role), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Initiative)
        .where(Initiative.club_id == club.id)
        .order_by(Initiative.start_date.desc(), Initiative.start_time.desc())
    )
    return result.scalars().all()


@router.post(
    "/initiatives", response_model=InitiativeOut, status_code=status.HTTP_201_CREATED
)
async def create_initiative(
    body: InitiativeCreate,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    # Check max 2 initiatives total for this club
    count_result = await db.execute(
        select(func.count())
        .select_from(Initiative)
        .where(Initiative.club_id == club.id)
    )
    count = count_result.scalar()
    if count >= 2:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Maximum 2 initiatives per club",
        )

    initiative = Initiative(
        title=body.title,
        description=body.description,
        category=body.category,
        start_date=body.start_date,
        start_time=body.start_time,
        end_date=body.end_date,
        end_time=body.end_time,
        status="pending",
        club_id=club.id,
    )
    db.add(initiative)
    await db.commit()
    await db.refresh(initiative)
    return initiative


@router.put("/initiatives/{initiative_id}", response_model=InitiativeOut)
async def update_initiative(
    initiative_id: int,
    body: InitiativeUpdate,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Initiative).where(
            Initiative.id == initiative_id, Initiative.club_id == club.id
        )
    )
    initiative = result.scalar_one_or_none()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found"
        )

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(initiative, field, value)

    await db.commit()
    await db.refresh(initiative)
    return initiative


@router.delete("/initiatives/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_initiative(
    initiative_id: int,
    club: Club = Depends(require_club_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Initiative).where(
            Initiative.id == initiative_id, Initiative.club_id == club.id
        )
    )
    initiative = result.scalar_one_or_none()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found"
        )
    await db.delete(initiative)
    await db.commit()
