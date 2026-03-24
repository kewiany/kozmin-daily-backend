from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        .where(Initiative.status == "approved")
        .order_by(Initiative.date.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
