from pydantic import BaseModel, field_validator


class AppleAuthRequest(BaseModel):
    identity_token: str
    email: str | None = None
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str | None = None
    full_name: str | None = None
    phone: str | None = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    needs_phone: bool
    user: UserResponse


class PhoneUpdateRequest(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) < 9:
            raise ValueError("Phone number must have at least 9 digits")
        return v
