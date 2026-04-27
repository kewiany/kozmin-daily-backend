from datetime import datetime

from pydantic import BaseModel


class DiscountOut(BaseModel):
    id: int
    title: str
    short_description: str | None = None
    long_description: str | None = None
    logo_url: str | None = None
    image_url: str | None = None
    address: str | None = None
    is_highlighted: bool = False
    is_pinned: bool = False
    priority: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}
