from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.club import Club
from app.schemas.club import ClubDetailOut, ClubOut

router = APIRouter(prefix="/api/v1/clubs", tags=["clubs"])


@router.get("", response_model=list[ClubOut])
async def list_clubs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Club)
        .where(Club.role != "admin", Club.is_archived == False)
        .order_by(Club.is_pinned.desc(), Club.priority.desc(), Club.name)
    )
    return result.scalars().all()


@router.get("/{club_id}", response_model=ClubDetailOut)
async def get_club(club_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Club)
        .where(Club.id == club_id)
        .options(selectinload(Club.events))
    )
    club = result.scalar_one_or_none()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    # Filter to only approved events
    club.events = [e for e in club.events if e.status == "approved" and not e.is_archived]
    return club
