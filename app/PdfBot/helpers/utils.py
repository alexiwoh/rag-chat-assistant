import html
import re


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
