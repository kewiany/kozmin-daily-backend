"""Scraper for Kozminski University events page."""

import datetime as dt
import re
from dataclasses import dataclass, field
from urllib.parse import parse_qs, unquote, urlparse

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.kozminski.edu.pl"
LISTING_URL = f"{BASE_URL}/pl/wydarzenia"


@dataclass
class ScrapedEvent:
    title: str
    url: str
    start_date: dt.date
    start_time: dt.time
    end_date: dt.date | None = None
    end_time: dt.time | None = None
    description: str | None = None
    location: str | None = None
    room: str | None = None
    mode: str | None = None
    language: str | None = None
    audience: str | None = None
    registration_url: str | None = None
    image_url: str | None = None


def _parse_date(text: str) -> dt.date:
    """Parse date from DD.MM.YYYY format."""
    text = text.strip()
    return dt.datetime.strptime(text, "%d.%m.%Y").date()


def _parse_time(text: str) -> dt.time:
    """Parse time from HH:MM format."""
    text = text.strip()
    return dt.datetime.strptime(text, "%H:%M").time()


def _parse_gcal_dates(gcal_url: str) -> tuple[dt.datetime, dt.datetime] | None:
    """Extract start/end datetimes from Google Calendar link."""
    try:
        parsed = urlparse(gcal_url)
        params = parse_qs(parsed.query)
        dates_str = params.get("dates", [None])[0]
        if not dates_str:
            return None
        start_str, end_str = dates_str.split("/")
        fmt = "%Y%m%dT%H%M%S"
        start = dt.datetime.strptime(start_str, fmt)
        end = dt.datetime.strptime(end_str, fmt)
        return start, end
    except (ValueError, TypeError, IndexError):
        return None


def _normalize_mode(raw: str) -> str | None:
    """Map Polish mode text to our schema values."""
    raw = raw.strip().lower()
    mapping = {"offline": "offline", "online": "online", "hybrydowe": "hybrid", "hybrid": "hybrid"}
    return mapping.get(raw)


def _normalize_language(raw: str) -> str | None:
    """Map language text to schema values."""
    raw = raw.strip().lower()
    if raw in ("pl", "polski"):
        return "pl"
    if raw in ("en", "angielski", "english"):
        return "en"
    return None


async def fetch_listing(client: httpx.AsyncClient) -> list[dict]:
    """Fetch the events listing page and extract basic event info."""
    resp = await client.get(LISTING_URL, follow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    events = []
    seen_urls = set()

    # Each event card has a .title div followed by .event-image with link
    for title_div in soup.select("div.title"):
        title_text = title_div.get_text(strip=True)
        if not title_text:
            continue

        # The event link is in the next sibling .event-image div
        event_image = title_div.find_next_sibling("div", class_="event-image")
        if not event_image:
            continue
        link_tag = event_image.find("a", href=True)
        if not link_tag:
            continue

        href = link_tag["href"]
        if not href.startswith("/pl/wydarzenia/") or "/kategoria/" in href:
            continue

        full_url = BASE_URL + href
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        # Date and time from event-content-wrap
        content_wrap = event_image.find_next_sibling("div", class_="event-content-wrap")
        date_text = None
        time_text = None
        if content_wrap:
            date_div = content_wrap.find("div", class_="date")
            if date_div:
                span = date_div.find("span")
                if span:
                    date_text = span.get_text(strip=True)
            time_div = content_wrap.find("div", class_="time")
            if time_div:
                span = time_div.find("span")
                if span:
                    time_text = span.get_text(strip=True)

        if not date_text or not time_text:
            continue

        try:
            start_date = _parse_date(date_text)
            start_time = _parse_time(time_text)
        except ValueError:
            continue

        # Skip past events
        if start_date < dt.date.today():
            continue

        events.append({
            "title": title_text,
            "url": full_url,
            "start_date": start_date,
            "start_time": start_time,
        })

    return events


async def fetch_detail(client: httpx.AsyncClient, url: str) -> dict:
    """Fetch an event detail page and extract additional info."""
    resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    detail: dict = {}

    # End time from Google Calendar link
    gcal_link = soup.find("a", href=re.compile(r"calendar\.google\.com"))
    if gcal_link:
        result = _parse_gcal_dates(gcal_link["href"].replace("&amp;", "&"))
        if result:
            start_dt, end_dt = result
            detail["end_date"] = end_dt.date()
            detail["end_time"] = end_dt.time()
            # Also update start if different (shouldn't be, but just in case)
            if start_dt.time() != dt.time(0, 0):
                detail["start_time_from_gcal"] = start_dt.time()

    # Location from header
    location_div = soup.select_one("div.event-content-wrap div.location span")
    if location_div:
        detail["location"] = location_div.get_text(strip=True)

    # Description from body
    body_section = soup.select_one("section.block-field-event-body div.body")
    if body_section:
        detail["description"] = body_section.get_text(separator="\n", strip=True)

    # Registration URL from CTA container
    cta_container = soup.select_one("div.event-cta-container")
    if cta_container:
        cta_link = cta_container.find("a", href=True)
        if cta_link:
            href = cta_link["href"]
            if href.startswith("http"):
                detail["registration_url"] = href

    # Mode (offline/online/hybrid)
    mode_section = soup.select_one("section.block-field-typ-wydarzenia .block-content")
    if mode_section:
        detail["mode"] = _normalize_mode(mode_section.get_text(strip=True))

    # Audience
    audience_section = soup.select_one("section.block-field-dla-kogo .block-content")
    if audience_section:
        detail["audience"] = audience_section.get_text(strip=True)

    # Language
    lang_section = soup.select_one("section.block-field-jezyki .block-content")
    if lang_section:
        detail["language"] = _normalize_language(lang_section.get_text(strip=True))

    # Place (separate from header location)
    place_section = soup.select_one("section.block-field-place .block-content")
    if place_section:
        detail["place"] = place_section.get_text(strip=True)

    # Image
    header_media = soup.select_one("div.media picture img")
    if header_media and header_media.get("src"):
        detail["image_url"] = BASE_URL + header_media["src"]

    return detail


async def scrape_events() -> list[ScrapedEvent]:
    """Full scrape: listing page + detail pages for each event."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        listing = await fetch_listing(client)
        print(f"Found {len(listing)} events on listing page")

        results = []
        for item in listing:
            try:
                detail = await fetch_detail(client, item["url"])
            except httpx.HTTPError as e:
                print(f"  Error fetching {item['url']}: {e}")
                continue

            # Determine location: prefer header location, fallback to place section
            location = detail.get("location") or detail.get("place")

            # Parse room from description body if it mentions "sala"
            room = None
            if detail.get("description"):
                room_match = re.search(r"sala\s+([A-Za-z0-9/]+)", detail["description"])
                if room_match:
                    room = room_match.group(1)

            # If location mentions ALK or Koźmińskiego, try to extract room
            if location and not room:
                room_match = re.search(r"sala\s+([A-Za-z0-9/]+)", location)
                if room_match:
                    room = room_match.group(1)

            end_date = detail.get("end_date", item["start_date"])
            end_time = detail.get("end_time", item["start_time"])

            event = ScrapedEvent(
                title=item["title"],
                url=item["url"],
                start_date=item["start_date"],
                start_time=item["start_time"],
                end_date=end_date,
                end_time=end_time,
                description=detail.get("description"),
                location=location,
                room=room,
                mode=detail.get("mode"),
                language=detail.get("language"),
                audience=detail.get("audience"),
                registration_url=detail.get("registration_url"),
                image_url=detail.get("image_url"),
            )
            results.append(event)
            print(f"  Scraped: {event.title}")

        return results
