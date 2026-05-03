from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/api/v1/waitlist", tags=["waitlist"])


class WaitlistRequest(BaseModel):
    email: EmailStr


class WaitlistResponse(BaseModel):
    ok: bool


@router.post("", response_model=WaitlistResponse)
async def join_waitlist(body: WaitlistRequest, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text(
            "INSERT INTO android_waitlist (email) VALUES (:email) "
            "ON CONFLICT (email) DO NOTHING"
        ),
        {"email": body.email},
    )
    await db.commit()
    return WaitlistResponse(ok=True)
