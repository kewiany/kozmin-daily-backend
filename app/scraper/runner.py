"""CLI runner for the Kozminski events scraper.

Usage: python -m app.scraper.runner
"""

import asyncio

from app.scraper.kozminski import scrape_events
from app.scraper.service import save_events


async def main():
    print("Starting Kozminski events scraper...")
    events = await scrape_events()
    print(f"\nSaving {len(events)} events to database...")
    stats = await save_events(events)
    print(f"\nDone! Added: {stats['added']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")


if __name__ == "__main__":
    asyncio.run(main())
