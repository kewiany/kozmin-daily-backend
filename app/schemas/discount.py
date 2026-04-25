from datetime import datetime

from pydantic import BaseModel


class DiscountOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    logo_url: str | None = None
    is_highlighted: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}
