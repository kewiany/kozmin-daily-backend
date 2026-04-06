from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token, verify_apple_token
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.firebase import verify_firebase_token
from app.models.user import User
from app.schemas.notification import FCMTokenRequest
from app.schemas.user import (
    AppleAuthRequest,
    AuthResponse,
    FirebaseAuthRequest,
    PhoneUpdateRequest,
    ProfileUpdateRequest,
    UserResponse,
)

router = APIRouter(prefix="/api/v1", tags=["mobile-auth"])


def _needs_profile(user: User) -> bool:
    return not user.first_name or not user.last_name or not user.email


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
            first_name=body.first_name,
            last_name=body.last_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        if body.email and not user.email:
            user.email = body.email
        if body.first_name and not user.first_name:
            user.first_name = body.first_name
        if body.last_name and not user.last_name:
            user.last_name = body.last_name
        await db.commit()
        await db.refresh(user)

    token = create_access_token(
        subject_id=user.id, role="user", entity_type="user"
    )

    return AuthResponse(
        access_token=token,
        needs_profile=_needs_profile(user),
        needs_phone=user.phone is None,
        user=UserResponse.model_validate(user),
    )


@router.post("/auth/firebase", response_model=AuthResponse)
async def firebase_auth(
    body: FirebaseAuthRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = verify_firebase_token(body.id_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase token: {e}",
        )

    firebase_uid = payload["uid"]
    phone_number = payload.get("phone_number")

    result = await db.execute(
        select(User).where(User.firebase_uid == firebase_uid)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(firebase_uid=firebase_uid, phone=phone_number)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token(
        subject_id=user.id, role="user", entity_type="user"
    )

    return AuthResponse(
        access_token=token,
        needs_profile=_needs_profile(user),
        needs_phone=user.phone is None,
        user=UserResponse.model_validate(user),
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.delete("/auth/me")
async def delete_account(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(user)
    await db.commit()
    return {"ok": True}


@router.put("/users/profile", response_model=UserResponse)
async def update_profile(
    body: ProfileUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user.first_name = body.first_name
    user.last_name = body.last_name
    user.email = body.email
    await db.commit()
    await db.refresh(user)
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


@router.put("/users/fcm-token")
async def update_fcm_token(
    body: FCMTokenRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user.fcm_token = body.fcm_token
    await db.commit()
    return {"ok": True}
