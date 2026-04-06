from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.news import News
from app.schemas.news import NewsOut

router = APIRouter(prefix="/api/v1/news", tags=["news"])


@router.get("", response_model=list[NewsOut])
async def list_news(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(News)
        .options(selectinload(News.club))
        .order_by(News.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{news_id}", response_model=NewsOut)
async def get_news(news_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(News)
        .options(selectinload(News.club))
        .where(News.id == news_id)
    )
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
    return news
