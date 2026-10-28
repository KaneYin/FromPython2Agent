from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .llm import LLMCallRecord


@dataclass
class TraceEvent:
    step: int
    type: Literal["think", "action", "observation", "final", "error", "budget_exceeded"]
    timestamp: float
    content: dict
    tokens: dict | None = None  # {"prompt": int, "completion": int, "total": int}
    latency_ms: float | None = None
    llm_call_id: str | None = None
    strategy_name: str | None = None
    tool_call_id: str | None = None


def _json_str(obj, indent: int | None = None) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def _truncate_system_in_messages(messages: list[dict], max_len: int = 500) -> list[dict]:
    result = []
    for msg in messages:
        m = dict(msg)
        if msg.get("role") == "system" and len(msg.get("content", "")) > max_len:
            content = msg["content"]
            m["content"] = content[:max_len] + f"... [truncated, {len(content)} chars total]"
        result.append(m)
    return result


class Trace:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []
        self.llm_calls: list[LLMCallRecord] = []
        self._query: str = ""
        self._strategy: str = ""

    def set_query(self, query: str) -> None:
        self._query = query

    def set_strategy(self, name: str) -> None:
        self._strategy = name

    def add(self, event: TraceEvent) -> None:
        self.events.append(event)

    def _get_call_by_id(self, call_id: str) -> LLMCallRecord | None:
        for rec in self.llm_calls:
            if rec.call_id == call_id:
                return rec
        return None

    def to_json(self) -> list[dict]:
        result: list[dict] = []
        for e in self.events:
            d: dict = {
                "step": e.step,
                "type": e.type,
                "timestamp": e.timestamp,
                "content": e.content,
            }
            if e.tokens is not None:
                d["tokens"] = e.tokens
            if e.latency_ms is not None:
                d["latency_ms"] = round(e.latency_ms, 1)
            if e.llm_call_id is not None:
                d["llm_call_id"] = e.llm_call_id
            if e.strategy_name is not None:
                d["strategy_name"] = e.strategy_name
            if e.tool_call_id is not None:
                d["tool_call_id"] = e.tool_call_id
            result.append(d)
        return result

    def summary(self) -> dict:
        total_steps = max((e.step for e in self.events), default=0)
        total_tokens = sum(
            e.tokens.get("total", 0) for e in self.events
            if e.type == "think" and e.tokens
        )
        total_latency = sum(
            e.latency_ms or 0 for e in self.events
            if e.type == "think"
        )
        finished = any(e.type == "final" for e in self.events)
        return {
            "total_steps": total_steps,
            "total_tokens": total_tokens,
            "total_latency_ms": round(total_latency, 1),
            "finished": finished,
        }

    def _render_llm_io(self, record: LLMCallRecord) -> list[str]:
        lines: list[str] = []
        call_id = record.call_id

        # Request block
        stop_str = _json_str(record.stop) if record.stop else "None"
        lines.append(f"<details>")
        lines.append(f"<summary>LLM Request (call_id: {call_id})</summary>")
        lines.append("")
        lines.append(f"**Model**: `{record.model}` | **Temperature**: {record.temperature} | **Stop**: `{stop_str}`")
        lines.append("")
        lines.append(f"**Messages** ({len(record.messages)} total):")
        lines.append("")
        display_msgs = record.messages
        lines.append("```json")
        lines.append(_json_str(display_msgs, indent=2))
        lines.append("```")
        lines.append("")
        lines.append("</details>")
        lines.append("")

        # Response block
        lines.append(f"<details>")
        lines.append(f"<summary>LLM Response (call_id: {call_id})</summary>")
        lines.append("")
        finish_str = record.finish_reason or "unknown"
        matched_str = f"`{record.matched_stop}`" if record.matched_stop else "None"
        lines.append(f"**Finish reason**: `{finish_str}` | **Matched stop**: {matched_str}")
        lines.append("")
        lines.append("**Content**:")
        lines.append("```")
        lines.append(record.content or "")
        lines.append("```")
        lines.append("")
        lines.append("</details>")

        return lines

    def _count_actions_in_step(self, step: int) -> int:
        return sum(1 for e in self.events if e.step == step and e.type == "action")

    def _action_index_in_step(self, step: int, event: TraceEvent) -> int:
        idx = 0
        for e in self.events:
            if e.step == step and e.type == "action":
                idx += 1
                if e is event:
                    return idx
        return 0

    def to_markdown(self) -> str:
        lines: list[str] = [f"# Agent Trace\n"]
        lines.append(f"**Query**: {self._query}")
        if self._strategy:
            lines.append(f"**Strategy**: {self._strategy}")
        s = self.summary()
        lines.append(
            f"**Steps**: {s['total_steps']} | "
            f"**Tokens**: {s['total_tokens']} | "
            f"**Latency**: {s['total_latency_ms']}ms\n"
        )

        # pre-compute action counts per step
        action_counts: dict[int, int] = {}
        for e in self.events:
            if e.type == "action":
                action_counts[e.step] = action_counts.get(e.step, 0) + 1

        # track action index for rendering numbering
        action_counters: dict[int, int] = {}

        for e in self.events:
            if e.type == "think":
                tokens_str = ""
                if e.tokens:
                    tokens_str = (
                        f" (prompt={e.tokens.get('prompt', 0)}, "
                        f"completion={e.tokens.get('completion', 0)}, "
                        f"total={e.tokens.get('total', 0)}"
                    )
                    if e.latency_ms is not None:
                        tokens_str += f", {e.latency_ms:.0f}ms"
                    tokens_str += ")"

                plan_phase = e.content.get("plan_phase")
                if plan_phase == "planning":
                    phase_label = " (planning)"
                elif plan_phase == "executing":
                    step_info = e.content.get("plan_step_info")
                    if step_info:
                        phase_label = f" (executing step {step_info[0]}/{step_info[1]})"
                    else:
                        phase_label = " (executing)"
                else:
                    phase_label = ""

                lines.append(f"## Step {e.step} — think{phase_label}{tokens_str}")
                thought = e.content.get("thought", "")
                if thought:
                    lines.append(f"**Thought**: {thought}")
                parse_error = e.content.get("parse_error")
                if parse_error:
                    lines.append(f"**Parse Error**: {parse_error}")

                plan_text = e.content.get("plan")
                if plan_text:
                    lines.append("**Generated Plan**:")
                    for line in plan_text:
                        lines.append(line)

                tool_calls = e.content.get("tool_calls")
                if tool_calls:
                    lines.append(f"**Tool Calls**: {len(tool_calls)}")

                # Render LLM I/O details
                if e.llm_call_id:
                    record = self._get_call_by_id(e.llm_call_id)
                    if record:
                        lines.append("")
                        lines.extend(self._render_llm_io(record))

            elif e.type == "action":
                total = action_counts.get(e.step, 1)
                action_counters[e.step] = action_counters.get(e.step, 0) + 1
                idx = action_counters[e.step]
                if total > 1:
                    lines.append(f"### Step {e.step} — action #{idx}")
                else:
                    lines.append(f"## Step {e.step} — action")
                lines.append(f"**Tool**: `{e.content.get('action', '')}`")
                lines.append(f"**Input**: `{_json_str(e.content.get('action_input', {}))}`")

            elif e.type == "observation":
                total_actions = action_counts.get(e.step, 1)
                if total_actions > 1:
                    lines.append(f"### Step {e.step} — observation #{action_counters.get(e.step, 0)}")
                else:
                    lines.append(f"## Step {e.step} — observation")
                lines.append(f"```\n{e.content.get('text', '')}\n```\n")

            elif e.type == "final":
                lines.append(f"## Step {e.step} — final")
                lines.append(f"**Final Answer**: {e.content.get('answer', '')}")

            elif e.type == "error":
                lines.append(f"## Step {e.step} — error")
                lines.append(f"**Error**: {e.content.get('message', '')}")

            elif e.type == "budget_exceeded":
                lines.append(f"## Step {e.step} — budget_exceeded")
                lines.append(f"**Reason**: {e.content.get('reason', '')}")

            lines.append("")

        return "\n".join(lines)
