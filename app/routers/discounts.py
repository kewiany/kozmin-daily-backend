from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.discount import Discount
from app.schemas.discount import DiscountOut

router = APIRouter(prefix="/api/v1/discounts", tags=["discounts"])


@router.get("", response_model=list[DiscountOut])
async def list_discounts(db: AsyncSession = Depends(get_db)):
    query = (
        select(Discount)
        .where(Discount.is_archived == False)
        .order_by(Discount.is_pinned.desc(), Discount.priority.desc(), Discount.title.asc())
    )
    result = await db.execute(query)
    return result.scalars().all()
