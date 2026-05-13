"""Scraper for Kozminski University news page."""

import datetime as dt
import re
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup

from app.scraper.logger import logger
from app.scraper.utils import html_to_clean_text

BASE_URL = "https://www.kozminski.edu.pl"
NEWS_URL = f"{BASE_URL}/pl/news"
PAGES_TO_FETCH = 3  # 5 articles per page → 15 total


@dataclass
class ScrapedNews:
    title: str
    url: str
    date: dt.date | None = None
    description: str | None = None
    preview: str | None = None


def _parse_date(text: str) -> dt.date:
    """Parse date from DD.MM.YYYY format."""
    return dt.datetime.strptime(text.strip(), "%d.%m.%Y").date()


async def fetch_news_listing(client: httpx.AsyncClient) -> list[dict]:
    """Fetch news listing pages and extract basic info."""
    items = []
    seen_urls: set[str] = set()

    for page in range(PAGES_TO_FETCH):
        url = NEWS_URL if page == 0 else f"{NEWS_URL}?page={page}"
        try:
            resp = await client.get(url, follow_redirects=True)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.warning("Error fetching news page %d: %s", page, e)
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        posts = soup.select("div.news-blog__post")

        for post in posts:
            article = post.find("article")
            if not article:
                continue

            # Title from div.post-title
            title_div = article.select_one("div.post-title")
            if not title_div:
                continue
            title = title_div.get_text(strip=True)
            if not title:
                continue

            # URL from button link
            link = article.select_one("div.button-wrapper a[href]")
            if not link:
                continue
            href = link["href"]
            if not href.startswith("/pl/news/"):
                continue
            full_url = BASE_URL + href
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            # Preview from teaser
            preview = None
            teaser = article.select_one("div.teaser div.block-content p")
            if teaser:
                preview = teaser.get_text(strip=True)

            items.append({
                "title": title,
                "url": full_url,
                "preview": preview,
            })

        logger.info("News page %d: found %d articles", page, len(posts))

    return items


async def fetch_news_detail(client: httpx.AsyncClient, url: str) -> dict:
    """Fetch a news detail page and extract content."""
    resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    detail: dict = {}

    # Date from div.date inside article > div.meta
    date_div = soup.select_one("article div.meta div.date")
    if date_div:
        date_text = date_div.get_text(strip=True)
        try:
            detail["date"] = _parse_date(date_text)
        except ValueError:
            pass

    # Body content from div.body elements inside the article
    bodies = soup.select("article section.block-text-block div.body")
    if bodies:
        # Combine all body sections
        combined_text_parts = []
        for body in bodies:
            text = html_to_clean_text(body)
            if text:
                combined_text_parts.append(text)
        if combined_text_parts:
            detail["description"] = "\n\n".join(combined_text_parts)

    return detail


async def scrape_news() -> list[ScrapedNews]:
    """Full scrape: listing pages + detail for each news article."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        listing = await fetch_news_listing(client)
        logger.info("Found %d news articles total", len(listing))

        results = []
        for item in listing:
            try:
                detail = await fetch_news_detail(client, item["url"])
            except httpx.HTTPError as e:
                logger.warning("Error fetching news %s: %s", item["url"], e)
                continue

            # Use listing preview, or generate from description
            preview = item.get("preview")
            description = detail.get("description")
            if not preview and description:
                preview = description[:200].rsplit(" ", 1)[0] if len(description) > 200 else description

            news = ScrapedNews(
                title=item["title"],
                url=item["url"],
                date=detail.get("date"),
                description=description,
                preview=preview,
            )
            results.append(news)
            logger.info("Scraped news: %s", news.title)

        return results
