from datetime import datetime

from pydantic import BaseModel, Field


class NewsCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=3000)
    preview: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=100)
    is_highlighted: bool = False


class NewsUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=3000)
    preview: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=100)
    is_highlighted: bool | None = None


class NewsOut(BaseModel):
    id: int
    title: str
    description: str
    preview: str | None = None
    author: str | None = None
    is_highlighted: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}
