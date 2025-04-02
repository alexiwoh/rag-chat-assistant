import html
import re
from collections import defaultdict

from ..constants import MAX_INPUT_LENGTH, NUMBER_OF_SOURCES_DISPLAY


def sanitize_text(text: str) -> str:
    """Sanitize user input or model output to prevent injection attacks or XSS."""
    if not text:
        return ""

    # Escape HTML special characters (prevents XSS in HTML templates)
    text = html.escape(text)

    # Strip potential SQL keywords (a very basic defense... expand on this later)
    sql_keywords = r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|--|;|UNION|EXEC|FETCH|DECLARE|CAST)\b"
    text = re.sub(sql_keywords, "[filtered]", text, flags=re.IGNORECASE)

    # Trim excess whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def validate_and_sanitize_query(raw_query: str) -> str:
    query = sanitize_text(raw_query)

    if not query.strip():
        raise ValueError("⚠️ Query cannot be empty.")
    if len(query) > MAX_INPUT_LENGTH:
        raise ValueError(f"⚠️ Query too long. Please limit to {MAX_INPUT_LENGTH} characters.")

    return query


def build_source_strings(source_documents) -> list[str]:
    source_to_pages = defaultdict(set)

    for doc in source_documents:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        if page is not None:
            source_to_pages[source].add(page)

    # Sort by the source name and limit
    top_sources = sorted(source_to_pages.items())[:NUMBER_OF_SOURCES_DISPLAY]

    result = []
    for source, pages in top_sources:
        if pages:
            page_list = sorted(pages)
            result.append(f"{source} (pages {', '.join(map(str, page_list))})")
        else:
            result.append(source)

    return result
