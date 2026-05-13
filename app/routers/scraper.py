from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.config import settings
from app.dependencies import require_admin_role
from app.models.club import Club
from app.scraper.kozminski import scrape_events
from app.scraper.logger import start_capture, stop_capture
from app.scraper.news import scrape_news
from app.scraper.service import save_events, save_news

router = APIRouter(prefix="/api/v1/admin/scraper", tags=["scraper"])


async def _run_all_scrapers() -> dict:
    """Run events + news scrapers and return combined stats."""
    start_capture()
    events = await scrape_events()
    event_stats = await save_events(events)
    events_log = stop_capture()

    start_capture()
    news = await scrape_news()
    news_stats = await save_news(news)
    news_log = stop_capture()

    return {
        "events": {**event_stats, "log": events_log},
        "news": {**news_stats, "log": news_log},
    }


@router.post("/run")
async def run_scraper(_admin: Club = Depends(require_admin_role)):
    """Manually trigger the scraper (admin JWT)."""
    return await _run_all_scrapers()


@router.post("/cron")
async def run_scraper_cron(x_scraper_secret: str = Header()):
    """Trigger scraper via cron secret (no expiry)."""
    if not settings.SCRAPER_SECRET or x_scraper_secret != settings.SCRAPER_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret")
    return await _run_all_scrapers()
