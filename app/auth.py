from datetime import datetime, timedelta, timezone

import bcrypt
import httpx
from jose import jwt, jwk, JWTError

from app.config import settings

_apple_keys_cache: dict | None = None


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(
    subject_id: int, role: str, entity_type: str = "club"
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(subject_id),
        "role": role,
        "entity_type": entity_type,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def _fetch_apple_public_keys() -> dict:
    global _apple_keys_cache
    if _apple_keys_cache is not None:
        return _apple_keys_cache
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://appleid.apple.com/auth/keys")
        resp.raise_for_status()
        _apple_keys_cache = resp.json()
        return _apple_keys_cache


async def verify_apple_token(identity_token: str, bundle_id: str) -> dict:
    """Verify Apple identity token and return decoded payload with 'sub'."""
    keys_data = await _fetch_apple_public_keys()

    # Get the key id from the token header
    headers = jwt.get_unverified_headers(identity_token)
    kid = headers.get("kid")

    # Find matching key
    matching_key = None
    for key in keys_data.get("keys", []):
        if key["kid"] == kid:
            matching_key = key
            break

    if matching_key is None:
        raise JWTError("No matching Apple public key found")

    public_key = jwk.construct(matching_key)

    # Decode and verify signature + issuer, check audience manually
    payload = jwt.decode(
        identity_token,
        public_key,
        algorithms=["RS256"],
        issuer="https://appleid.apple.com",
        options={"verify_aud": False},
    )

    # Manual audience check
    token_aud = payload.get("aud")
    if token_aud != bundle_id:
        raise JWTError(
            f"Invalid audience: got '{token_aud}', expected '{bundle_id}'"
        )

    return payload
