from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    preview: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(300), nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    preview_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
