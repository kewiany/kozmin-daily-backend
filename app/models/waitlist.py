from sqlalchemy import Column, Integer, String, DateTime, func

from app.database import Base


class AndroidWaitlist(Base):
    __tablename__ = "android_waitlist"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
