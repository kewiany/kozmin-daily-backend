"""Service layer: saves scraped events to the database with deduplication."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.club import Club
from app.models.event import Event
from app.scraper.kozminski import ScrapedEvent

UNIVERSITY_LOGIN = "__university__"


async def get_university_club(db: AsyncSession) -> Club:
    """Get the university club record used for scraped events."""
    result = await db.execute(select(Club).where(Club.login == UNIVERSITY_LOGIN))
    club = result.scalar_one_or_none()
    if not club:
        raise RuntimeError(
            f"University club not found (login={UNIVERSITY_LOGIN}). "
            "Run 'alembic upgrade head' first."
        )
    return club


async def event_exists(db: AsyncSession, title: str, start_date, club_id: int) -> bool:
    """Check if an event with the same title, start_date, and club_id already exists."""
    result = await db.execute(
        select(Event).where(
            Event.title == title,
            Event.start_date == start_date,
            Event.club_id == club_id,
        )
    )
    return result.scalar_one_or_none() is not None


def _map_audience(raw: str | None) -> list[str] | None:
    """Map scraped audience text to schema values."""
    if not raw:
        return None
    raw = raw.lower()
    if "otwarte" in raw or "open" in raw:
        return ["open"]
    if "student" in raw:
        return ["students"]
    if "absolwent" in raw or "alumni" in raw:
        return ["alumni"]
    if "kandydat" in raw or "candidate" in raw:
        return ["candidates"]
    return None


async def save_events(scraped: list[ScrapedEvent]) -> dict:
    """Save scraped events to DB. Returns stats dict."""
    stats = {"total": len(scraped), "added": 0, "skipped": 0, "errors": 0}

    async with async_session() as db:
        club = await get_university_club(db)

        for ev in scraped:
            try:
                if await event_exists(db, ev.title, ev.start_date, club.id):
                    stats["skipped"] += 1
                    continue

                # Determine address fields
                address_name = None
                address_city = "Warszawa"
                if ev.location:
                    address_name = ev.location

                event = Event(
                    title=ev.title,
                    description=ev.description,
                    start_date=ev.start_date,
                    start_time=ev.start_time,
                    end_date=ev.end_date or ev.start_date,
                    end_time=ev.end_time or ev.start_time,
                    status="approved",
                    audience=_map_audience(ev.audience),
                    mode=ev.mode,
                    language=ev.language,
                    address_name=address_name,
                    address_city=address_city,
                    room_number=ev.room,
                    club_id=club.id,
                    # CTA1: link to university event page
                    cta_enabled=True,
                    cta_button_text="Strona wydarzenia",
                    cta_link_url=ev.url,
                    # CTA2: registration link (if available)
                    cta2_enabled=bool(ev.registration_url),
                    cta2_button_text="Rejestracja" if ev.registration_url else None,
                    cta2_link_url=ev.registration_url,
                )
                db.add(event)
                stats["added"] += 1

            except Exception as e:
                print(f"  Error saving '{ev.title}': {e}")
                stats["errors"] += 1

        await db.commit()

    return stats
