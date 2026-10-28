"""Web search tool using Tavily API (httpx, no SDK)."""
from __future__ import annotations

import os

import httpx

from .base import Tool

_TAVILY_URL = "https://api.tavily.com/search"
_TIMEOUT_SECONDS = 10
_MAX_CONTENT_CHARS = 200


def _web_search(query: str, max_results: int = 3) -> str:
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return "Error: TAVILY_API_KEY not set"

    # Clamp max_results to 1-5
    max_results = max(1, min(5, max_results))

    payload = {
        "query": query,
        "max_results": max_results,
        "include_answer": False,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        resp = httpx.post(
            _TAVILY_URL,
            json=payload,
            headers=headers,
            timeout=_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        return "Error: Search timed out"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

    if resp.status_code != 200:
        return f"Error: Search API returned {resp.status_code}"

    try:
        data = resp.json()
    except Exception:
        return "Error: Failed to parse search response"

    results = data.get("results", [])
    if not results:
        return "(no results found)"

    lines: list[str] = []
    for i, item in enumerate(results, 1):
        title = item.get("title", "(no title)")
        url = item.get("url", "")
        content = item.get("content", "")
        # Truncate content for LLM readability
        if len(content) > _MAX_CONTENT_CHARS:
            content = content[:_MAX_CONTENT_CHARS] + "..."
        lines.append(f"[{i}] Title: {title}")
        lines.append(f"    URL: {url}")
        lines.append(f"    Summary: {content}")
        lines.append("")

    return "\n".join(lines).strip()


WEB_SEARCH_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The search query",
        },
        "max_results": {
            "type": "integer",
            "description": "Maximum number of results to return (1-5, default 3)",
            "default": 3,
        },
    },
    "required": ["query"],
}

web_search_tool = Tool(
    name="web_search",
    description=(
        "Search the web using Tavily and return top results with titles, URLs, and summaries. "
        "Use this tool when you need to find information from the internet."
    ),
    parameters=WEB_SEARCH_PARAMETERS,
    func=_web_search,
)
