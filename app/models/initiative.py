import datetime as dt
from datetime import datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Initiative(Base):
    __tablename__ = "initiatives"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    start_time: Mapped[dt.time] = mapped_column(Time, nullable=False)
    end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    end_time: Mapped[dt.time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    audience: Mapped[str | None] = mapped_column(String(50), nullable=True)
    event_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    club = relationship("Club", back_populates="initiatives")
