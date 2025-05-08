# src/utils.py
import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Basic URL validation using urllib and regex.
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


def sanitize_text(text: str) -> str:
    """
    Clean up extracted text: collapse whitespace and remove control characters.
    """
    # collapse multiple spaces/newlines
    cleaned = re.sub(r"\s+", " ", text)
    # strip leading/trailing whitespace
    return cleaned.strip()