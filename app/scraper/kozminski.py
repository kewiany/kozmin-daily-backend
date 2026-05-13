"""Scraper for Kozminski University events page."""

import datetime as dt
import re
from dataclasses import dataclass, field
from urllib.parse import parse_qs, unquote, urlparse

import httpx
from bs4 import BeautifulSoup

from app.scraper.logger import logger

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


def _html_to_clean_text(body_tag) -> str:
    """Convert HTML body to clean plain text for mobile display."""
    # Remove all emoji (decorative ones that look bad on mobile)
    EMOJI_RE = re.compile(
        r"[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0000200D\U00002600-\U000026FF\U00002B50\U00002B55\U000023F0-\U000023FA"
        r"\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]+",
        re.UNICODE,
    )

    # Process <br> → newline before extracting text
    for br in body_tag.find_all("br"):
        br.replace_with("\n")

    # Process each <p> and <li> into paragraphs
    paragraphs = []
    consecutive_bullets = 0
    for el in body_tag.find_all(["p", "li"]):
        text = el.get_text(separator=" ").strip()
        if not text or text == "\xa0":
            continue
        # Clean up
        text = text.replace("\xa0", " ")
        text = EMOJI_RE.sub(" ", text)  # replace emoji with space
        text = re.sub(r" {2,}", " ", text)  # collapse multiple spaces
        text = text.strip()
        if text:
            # Prefix list items with bullet
            is_bullet = el.name == "li"
            if is_bullet:
                text = f"• {text}"
                consecutive_bullets += 1
            else:
                consecutive_bullets = 0
            paragraphs.append(text)

    # Join: single newline between consecutive bullets, double between paragraphs
    lines = []
    for i, para in enumerate(paragraphs):
        if i > 0:
            prev_is_bullet = paragraphs[i - 1].startswith("• ")
            curr_is_bullet = para.startswith("• ")
            if prev_is_bullet and curr_is_bullet:
                lines.append("\n")
            else:
                lines.append("\n\n")
        lines.append(para)

    result = "".join(lines)
    # Collapse 3+ newlines into 2
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def _remove_redundant_lines(text: str, title: str, location: str | None,
                           room: str | None, start_date: dt.date,
                           start_time: dt.time) -> str:
    """Remove description lines that just repeat structured fields."""
    date_strs = {
        start_date.strftime("%d.%m.%Y"),
        start_date.strftime("%d.%m.%y"),
        start_date.strftime("%-d %B %Y"),  # "13 May 2025"
    }
    time_str = start_time.strftime("%H:%M")

    lines = text.split("\n")
    filtered = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            filtered.append(line)
            continue

        # Skip lines that are just the title repeated
        if stripped.lower() == title.lower():
            continue

        # Skip lines that are purely date/time/location info (short + matches)
        if len(stripped) < 80:
            lower = stripped.lower()
            is_redundant = False

            # "Termin: 13 maja 2025" / "Data: ..." / "Godzina: 17:00"
            if any(d in stripped for d in date_strs) and any(
                k in lower for k in ("termin", "data", "date", "kiedy", "when")
            ):
                is_redundant = True
            if time_str in stripped and any(
                k in lower for k in ("godzina", "godz", "time", "hour")
            ):
                is_redundant = True
            # "Miejsce: ALK, sala A/22"
            if any(k in lower for k in ("miejsce:", "location:", "where:", "venue:")):
                is_redundant = True
            # Lines that are just the location name
            if location and stripped.lower() == location.lower():
                is_redundant = True

            if is_redundant:
                continue

        filtered.append(line)

    result = "\n".join(filtered)
    # Collapse excessive blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


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
        detail["description_raw"] = body_section

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
        logger.info("Found %d events on listing page", len(listing))

        results = []
        for item in listing:
            try:
                detail = await fetch_detail(client, item["url"])
            except httpx.HTTPError as e:
                logger.warning("Error fetching %s: %s", item["url"], e)
                continue

            # Determine location: prefer header location, fallback to place section
            location = detail.get("location") or detail.get("place")

            end_date = detail.get("end_date", item["start_date"])
            end_time = detail.get("end_time", item["start_time"])

            # Parse room from raw description HTML
            room = None
            description = None
            body_tag = detail.get("description_raw")
            if body_tag:
                raw_text = body_tag.get_text()
                room_match = re.search(r"sala\s+([A-Za-z0-9/]+)", raw_text)
                if room_match:
                    room = room_match.group(1)

                # Convert HTML to clean text
                description = _html_to_clean_text(body_tag)

                # Remove lines that duplicate structured fields
                description = _remove_redundant_lines(
                    description,
                    title=item["title"],
                    location=location,
                    room=room,
                    start_date=item["start_date"],
                    start_time=item["start_time"],
                )

            # Extract location/room from body text when not in structured fields
            if body_tag and not location:
                raw_text = body_tag.get_text()
                miejsce_match = re.search(
                    r"(?:Miejsce|Location|Venue|Gdzie)\s*:\s*(.+)",
                    raw_text,
                )
                if miejsce_match:
                    miejsce = miejsce_match.group(1).strip().split("\n")[0].strip()
                    location = miejsce
                    # Extract room from "ALK, Aula II" or "ALK, sala D/204"
                    room_in_loc = re.search(r"[,;]\s*((?:sala\s+)?(?:Aula\b|[A-Z]/?\d+).*)$", miejsce, re.IGNORECASE)
                    if room_in_loc and not room:
                        room = room_in_loc.group(1).strip()

            # If location mentions sala/aula, extract room and clean location
            if location and not room:
                room_match = re.search(r"sala\s+([A-Za-z0-9/]+)", location)
                if room_match:
                    room = room_match.group(1)
            if location and room:
                # Remove room portion from location: "ALK, sala D/204" → "ALK"
                location = re.sub(r"[,;]\s*(?:sala\s+)?(?:Aula\s+\S+|[A-Za-z]/?\d+\S*)\s*$", "", location, flags=re.IGNORECASE).strip()
                location = re.sub(r"^(?:sala\s+)?(?:Aula\s+\S+|[A-Za-z]/?\d+\S*)\s*[,;]\s*", "", location, flags=re.IGNORECASE).strip()
                # If cleaning left nothing or just punctuation, default to ALK
                if not location or location in (",", ";"):
                    location = "Akademia Leona Koźmińskiego"

            # If location is just a room/aula name, set ALK as the address
            if location:
                loc_clean = location.strip()
                loc_lower = loc_clean.lower()
                is_room_only = (
                    re.match(r"^(sala\s+)?[a-z]\s*/?\s*\d+", loc_lower)  # "D/217", "sala D 202"
                    or re.match(r"^(sala\s+)?aula\b", loc_lower)          # "Aula II", "sala Aula I"
                    or re.match(r"^[a-z]\d{2,}$", loc_lower)              # "D217"
                )
                if is_room_only:
                    if not room:
                        room = re.sub(r"^sala\s+", "", loc_clean, flags=re.IGNORECASE).strip()
                    location = "Akademia Leona Koźmińskiego"

            # No location at all → default to ALK (it's a university event page)
            if not location:
                location = "Akademia Leona Koźmińskiego"

            # Infer mode from title/description when not in structured fields
            mode = detail.get("mode")
            if not mode:
                all_text = (item["title"] + " " + (description or "")).lower()
                if "online" in all_text and "offline" not in all_text:
                    mode = "online"
                elif "hybryd" in all_text:
                    mode = "hybrid"

            # Infer language from title/description when not in structured fields
            language = detail.get("language")
            if not language:
                title_lower = item["title"].lower()
                desc_lower = (description or "").lower()
                # English indicators in title
                en_words = ["open day", "workshop", "webinar", "meeting", "lecture",
                            "summit", "masterclass", "bootcamp", "challenge"]
                pl_words = ["zapraszamy", "wykład", "spotkanie", "warsztaty",
                            "konferencja", "dzień", "konkurs"]
                if any(w in title_lower for w in en_words):
                    language = "en"
                elif any(w in title_lower for w in pl_words):
                    language = "pl"
                elif any(w in desc_lower for w in pl_words):
                    language = "pl"

            event = ScrapedEvent(
                title=item["title"],
                url=item["url"],
                start_date=item["start_date"],
                start_time=item["start_time"],
                end_date=end_date,
                end_time=end_time,
                description=description,
                location=location,
                room=room,
                mode=mode,
                language=language,
                audience=detail.get("audience"),
                registration_url=detail.get("registration_url"),
                image_url=detail.get("image_url"),
            )
            results.append(event)
            logger.info("Scraped: %s", event.title)

        return results
