"""Shared utilities for scrapers."""

import re


def html_to_clean_text(body_tag) -> str:
    """Convert HTML body to clean plain text for mobile display."""
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
        text = re.sub(r"\s*" + EMOJI_RE.pattern + r"\s*", " ", text)  # remove emoji + surrounding spaces
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
