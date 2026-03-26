from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token, verify_apple_token
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import (
    AppleAuthRequest,
    AuthResponse,
    PhoneUpdateRequest,
    UserResponse,
)

router = APIRouter(prefix="/api/v1", tags=["mobile-auth"])


@router.post("/auth/apple", response_model=AuthResponse)
async def apple_auth(
    body: AppleAuthRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = await verify_apple_token(
            body.identity_token, settings.APPLE_BUNDLE_ID
        )
    except (JWTError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Apple token: {e}",
        )

    apple_user_id = payload["sub"]

    result = await db.execute(
        select(User).where(User.apple_user_id == apple_user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            apple_user_id=apple_user_id,
            email=body.email,
            full_name=body.full_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # Update email/name if Apple provides them (user may have changed)
        if body.email and not user.email:
            user.email = body.email
        if body.full_name and not user.full_name:
            user.full_name = body.full_name
        await db.commit()
        await db.refresh(user)

    token = create_access_token(
        subject_id=user.id, role="user", entity_type="user"
    )

    return AuthResponse(
        access_token=token,
        needs_phone=user.phone is None,
        user=UserResponse.model_validate(user),
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.put("/users/phone", response_model=UserResponse)
async def update_phone(
    body: PhoneUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user.phone = body.phone
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)
