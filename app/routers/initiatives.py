from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.initiative import Initiative
from app.schemas.initiative import InitiativeOut

router = APIRouter(prefix="/api/v1/initiatives", tags=["initiatives"])


@router.get("", response_model=list[InitiativeOut])
async def list_initiatives(
    skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.status == "approved")
        .order_by(Initiative.start_date.desc(), Initiative.start_time.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/all", response_model=list[InitiativeOut])
async def list_all_initiatives(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.status == "approved")
    )
    if date_from:
        query = query.where(Initiative.start_date >= date_from)
    if date_to:
        query = query.where(Initiative.start_date <= date_to)
    query = query.order_by(Initiative.start_date.asc(), Initiative.start_time.asc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/upcoming", response_model=list[InitiativeOut])
async def list_upcoming_initiatives(
    skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.status == "approved", Initiative.start_date >= date.today())
        .order_by(Initiative.start_date.asc(), Initiative.start_time.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/past", response_model=list[InitiativeOut])
async def list_past_initiatives(
    skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.status == "approved", Initiative.start_date < date.today())
        .order_by(Initiative.start_date.desc(), Initiative.start_time.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{initiative_id}", response_model=InitiativeOut)
async def get_initiative(initiative_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Initiative)
        .options(selectinload(Initiative.club))
        .where(Initiative.id == initiative_id, Initiative.status == "approved")
    )
    initiative = result.scalar_one_or_none()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found"
        )
    return initiative
