from __future__ import annotations

import re

from .base import Tool


def _count_words(text: str) -> int:
    # English words split by whitespace
    en_words = re.findall(r"[a-zA-Z]+", text)
    # Chinese characters (each char counts as a word)
    cn_chars = re.findall(r"[一-鿿]", text)
    return len(en_words) + len(cn_chars)


def _text_stats(text: str) -> str:
    chars = len(text)
    words = _count_words(text)
    lines = len(text.splitlines()) if text else 0
    return f"chars={chars}, words={words}, lines={lines}"


TEXT_STATS_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "The text to analyze",
        }
    },
    "required": ["text"],
}


text_stats_tool = Tool(
    name="text_stats",
    description=(
        "Analyzes text and returns character count, word count, and line count. "
        "Supports both English and Chinese text. "
        "Use this tool when you need to count characters, words, or lines in a given text."
    ),
    parameters=TEXT_STATS_PARAMETERS,
    func=_text_stats,
)
