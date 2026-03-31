from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin_role
from app.firebase import send_broadcast
from app.models.club import Club
from app.models.event import Event
from app.models.initiative import Initiative
from app.models.user import User
from app.schemas.event import EventOut
from app.schemas.initiative import InitiativeOut
from app.schemas.notification import (
    BroadcastNotificationRequest,
    BroadcastNotificationResponse,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


class PendingResponse(BaseModel):
    events: list[EventOut]
    initiatives: list[InitiativeOut]


@router.get("/pending", response_model=PendingResponse)
async def list_pending(
    _admin: Club = Depends(require_admin_role), db: AsyncSession = Depends(get_db)
):
    events_result = await db.execute(
        select(Event).where(Event.status == "pending").order_by(Event.created_at.desc())
    )
    initiatives_result = await db.execute(
        select(Initiative)
        .where(Initiative.status == "pending")
        .order_by(Initiative.created_at.desc())
    )
    return PendingResponse(
        events=events_result.scalars().all(),
        initiatives=initiatives_result.scalars().all(),
    )


@router.put("/events/{event_id}/approve", response_model=EventOut)
async def approve_event(
    event_id: int,
    _admin: Club = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    event.status = "approved"
    await db.commit()
    await db.refresh(event)
    return event


@router.put("/events/{event_id}/reject", response_model=EventOut)
async def reject_event(
    event_id: int,
    _admin: Club = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    event.status = "rejected"
    await db.commit()
    await db.refresh(event)
    return event


@router.put("/initiatives/{initiative_id}/approve", response_model=InitiativeOut)
async def approve_initiative(
    initiative_id: int,
    _admin: Club = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Initiative).where(Initiative.id == initiative_id)
    )
    initiative = result.scalar_one_or_none()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found"
        )
    initiative.status = "approved"
    await db.commit()
    await db.refresh(initiative)
    return initiative


@router.put("/initiatives/{initiative_id}/reject", response_model=InitiativeOut)
async def reject_initiative(
    initiative_id: int,
    _admin: Club = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Initiative).where(Initiative.id == initiative_id)
    )
    initiative = result.scalar_one_or_none()
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found"
        )
    initiative.status = "rejected"
    await db.commit()
    await db.refresh(initiative)
    return initiative


@router.post(
    "/notifications/broadcast", response_model=BroadcastNotificationResponse
)
async def broadcast_notification(
    body: BroadcastNotificationRequest,
    _admin: Club = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.fcm_token.is_not(None))
    )
    users = result.scalars().all()
    tokens = [u.fcm_token for u in users]

    if not tokens:
        return BroadcastNotificationResponse(
            success=0, failure=0, total_tokens=0
        )

    data: dict[str, str] | None = None
    if body.event_id is not None:
        data = {"type": "event", "id": str(body.event_id)}
    elif body.initiative_id is not None:
        data = {"type": "initiative", "id": str(body.initiative_id)}

    success, failure, bad_tokens = send_broadcast(tokens, body.title, body.body, data)

    if bad_tokens:
        for user in users:
            if user.fcm_token in bad_tokens:
                user.fcm_token = None
        await db.commit()

    return BroadcastNotificationResponse(
        success=success, failure=failure, total_tokens=len(tokens)
    )
