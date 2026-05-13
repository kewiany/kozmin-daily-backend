"""CLI runner for the Kozminski scraper (events + news).

Usage: python -m app.scraper.runner
"""

import asyncio

from app.scraper.kozminski import scrape_events
from app.scraper.logger import logger
from app.scraper.news import scrape_news
from app.scraper.service import save_events, save_news


async def main():
    # Events
    logger.info("Starting Kozminski events scraper...")
    events = await scrape_events()
    logger.info("Saving %d events to database...", len(events))
    event_stats = await save_events(events)
    logger.info(
        "Events — Added: %d, Updated: %d, Skipped: %d, Errors: %d",
        event_stats["added"], event_stats["updated"],
        event_stats["skipped"], event_stats["errors"],
    )

    # News
    logger.info("Starting Kozminski news scraper...")
    news = await scrape_news()
    logger.info("Saving %d news to database...", len(news))
    news_stats = await save_news(news)
    logger.info(
        "News — Added: %d, Updated: %d, Skipped: %d, Errors: %d",
        news_stats["added"], news_stats["updated"],
        news_stats["skipped"], news_stats["errors"],
    )


if __name__ == "__main__":
    asyncio.run(main())
