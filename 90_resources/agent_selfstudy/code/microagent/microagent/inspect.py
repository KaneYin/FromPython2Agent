from __future__ import annotations

import json

from .llm import LLMCallRecord


def print_call(record: LLMCallRecord, show_messages: bool = True) -> None:
    print(f"=== LLM Call {record.call_id} ===")
    print(f"Model: {record.model} | Temperature: {record.temperature}")
    print(f"Latency: {record.latency_ms:.1f}ms")
    print(f"Finish reason: {record.finish_reason}")
    if record.matched_stop:
        print(f"Matched stop: {record.matched_stop}")
    print(f"Usage: prompt={record.usage.get('prompt_tokens', 0)}, "
          f"completion={record.usage.get('completion_tokens', 0)}, "
          f"total={record.usage.get('total_tokens', 0)}")

    if show_messages:
        print(f"\nMessages ({len(record.messages)} total):")
        for i, msg in enumerate(record.messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if len(content) > 120:
                content = content[:120] + "..."
            print(f"  [{i}] {role}: {content}")

    print(f"\nResponse content:")
    print(record.content)
    print(f"=== End Call {record.call_id} ===\n")


def diff_messages(prev: list[dict], curr: list[dict]) -> str:
    prefix_len = 0
    for i in range(min(len(prev), len(curr))):
        if prev[i] == curr[i]:
            prefix_len = i + 1
        else:
            break

    added = curr[prefix_len:]
    if not added:
        return "No changes"

    parts: list[str] = []
    for msg in added:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        preview = content[:80] + ("..." if len(content) > 80 else "")
        parts.append(f"+1 {role}: {preview}")

    return "\n".join(parts)
