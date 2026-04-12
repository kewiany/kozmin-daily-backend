from datetime import datetime

from pydantic import BaseModel


class NewsCreate(BaseModel):
    title: str
    description: str
    author: str | None = None
    is_highlighted: bool = False


class NewsUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    is_highlighted: bool | None = None


class NewsOut(BaseModel):
    id: int
    title: str
    description: str
    author: str | None = None
    is_highlighted: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}
