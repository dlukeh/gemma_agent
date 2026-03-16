import requests
import trafilatura
from pathlib import Path

MAX_CHARS = 1500  # Reduced slightly for better focus on 8B/12B models


def visit_webpage(url: str) -> str:
    """
    Fetches a URL and uses trafilatura to extract clean, structural Markdown.
    This removes 'fluff' like navbars and ads automatically.
    """
    try:
        # 1. Fetch the raw HTML
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        # 2. Extract content using trafilatura
        # output_format='markdown' preserves headers and lists for the LLM
        # include_links=False keeps the context window from getting cluttered with URLs
        downloaded = response.text
        result = trafilatura.extract(
            downloaded, output_format="markdown", include_links=False
        )

        if not result:
            return "Error: Could not extract meaningful content from this page."

        # 3. Clean up whitespace and truncate
        cleaned = result.strip()

        if len(cleaned) > MAX_CHARS:
            return (
                cleaned[:MAX_CHARS]
                + "\n\n[Content truncated for context window efficiency]"
            )

        return cleaned

    except Exception as e:
        return f"Failed to visit {url}: {str(e)}"
