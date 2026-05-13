from fastapi import APIRouter, Depends

from app.dependencies import require_admin_role
from app.models.club import Club
from app.scraper.kozminski import scrape_events
from app.scraper.service import save_events

router = APIRouter(prefix="/api/v1/admin/scraper", tags=["scraper"])


@router.post("/run")
async def run_scraper(_admin: Club = Depends(require_admin_role)):
    """Manually trigger the Kozminski events scraper."""
    events = await scrape_events()
    stats = await save_events(events)
    return stats
