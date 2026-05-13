"""CLI runner for the Kozminski events scraper.

Usage: python -m app.scraper.runner
"""

import asyncio

from app.scraper.kozminski import scrape_events
from app.scraper.logger import logger
from app.scraper.service import save_events


async def main():
    logger.info("Starting Kozminski events scraper...")
    events = await scrape_events()
    logger.info("Saving %d events to database...", len(events))
    stats = await save_events(events)
    logger.info(
        "Done! Added: %d, Updated: %d, Skipped: %d, Errors: %d",
        stats["added"], stats["updated"], stats["skipped"], stats["errors"],
    )


if __name__ == "__main__":
    asyncio.run(main())
