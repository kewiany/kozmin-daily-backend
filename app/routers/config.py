from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.feature_flag import FeatureFlag
from app.schemas.feature_flag import ConfigResponse

router = APIRouter(prefix="/api/v1/config", tags=["config"])


@router.get("", response_model=ConfigResponse)
async def get_config(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureFlag))
    flags = {row.key: row.value for row in result.scalars().all()}
    return ConfigResponse(flags=flags)
