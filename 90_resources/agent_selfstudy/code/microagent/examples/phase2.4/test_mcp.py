"""Phase 2.4 verification — test MCP Client integration with Agent."""
from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Ensure project root on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
load_dotenv()

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.memory import Memory
from microagent.mcp import MCPToolRegistry, MCPServerConfig
from microagent.strategies import FunctionCallingStrategy
from microagent.tools.base import ToolRegistry


# ── Config ─────────────────────────────────────────────────────────

_OUTPUT_DIR = Path(__file__).parent / "output"
MOCK_SERVER_SCRIPT = str(Path(__file__).parent / "mock_mcp_server.py")


def _log(msg: str) -> None:
    print(msg, flush=True)


def _first_line(text: str, max_len: int = 80) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:max_len] + ("..." if len(line) > max_len else "")
    return ""


# ── Detail file writer (same pattern as Phase 2.3) ─────────────────

class DetailWriter:
    def __init__(self, output_dir: Path) -> None:
        self._dir = output_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lines: list[str] = []
        self._current_name: str = ""

    def start_case(self, name: str, query: str) -> None:
        self._current_name = name
        self._lines = [
            f"{'='*60}",
            f"  Case: {name}",
            f"  Query: {query}",
            f"{'='*60}",
            "",
        ]

    def write_step(self, event) -> None:
        if event.type == "think":
            thought = event.content.get("thought", "")
            tokens_info = ""
            if event.tokens:
                tokens_info = f"  [{event.tokens.get('total', 0)} tokens, {event.latency_ms:.0f}ms]"
            if thought:
                self._lines.append(f"  Step {event.step} — Think{tokens_info}:")
                for line in thought.splitlines():
                    self._lines.append(f"    {line}")
            tool_calls = event.content.get("tool_calls")
            if tool_calls:
                self._lines.append(f"  Step {event.step} — Tool Calls:")
                for tc in tool_calls:
                    args = json.dumps(tc["arguments"], ensure_ascii=False)
                    self._lines.append(f"    {tc['name']}({args})")
        elif event.type == "action":
            action = event.content.get("action", "")
            inp = json.dumps(event.content.get("action_input", {}), ensure_ascii=False)
            self._lines.append(f"  Step {event.step} — Action: {action}({inp})")
        elif event.type == "observation":
            text = event.content.get("text", "")
            self._lines.append(f"  Step {event.step} — Observation:")
            for line in text.splitlines():
                self._lines.append(f"    {line}")
        elif event.type == "final":
            self._lines.append(f"  Step {event.step} — Final Answer:")
            answer = event.content.get("answer", "")
            for line in answer.splitlines():
                self._lines.append(f"    {line}")
        elif event.type == "error":
            self._lines.append(f"  Step {event.step} — Error: {event.content.get('message', '')}")
        elif event.type == "budget_exceeded":
            self._lines.append(f"  Step {event.step} — Budget Exceeded: {event.content.get('reason', '')}")

    def finish_case(self, tag: str, summary: dict, elapsed: float, answer: str | None) -> None:
        self._lines.append("")
        self._lines.append(f"  Result: {tag}")
        self._lines.append(
            f"  Steps: {summary['total_steps']}  |  Tokens: {summary['total_tokens']}  "
            f"|  Latency: {summary['total_latency_ms']:.0f}ms  |  Wall: {elapsed:.1f}s"
        )
        if answer:
            self._lines.append(f"  Answer: {answer}")
        self._lines.append("")
        path = self._dir / f"{self._current_name}.txt"
        path.write_text("\n".join(self._lines), encoding="utf-8")

    def write_summary(self, results: list[dict], pass_count: int, fail_count: int) -> None:
        lines = [
            f"{'='*60}",
            f"  Phase 2.4 MCP Test Summary",
            f"  RESULT: {pass_count} passed, {fail_count} failed  ({pass_count}/{len(results)})",
            f"{'='*60}",
            "",
        ]
        for r in results:
            icon = "PASS" if r["ok"] else "FAIL"
            lines.append(f"  [{icon}] {r['name']:<20} {r['steps']} steps  {r['elapsed']:.1f}s")
            if r["answer"]:
                lines.append(f"       {r['answer']}")
            lines.append(f"       Detail: output/{r['name']}.txt")
            lines.append("")
        path = self._dir / "summary.txt"
        path.write_text("\n".join(lines), encoding="utf-8")


# ── Test cases ─────────────────────────────────────────────────────

test_cases = [
    ("echo_tool",     "用 echo 工具把 'hello MCP' 回传给我"),
    ("add_tool",      "用 add 工具算 123 加 456"),
    ("multi_mcp",     "先用 echo 说一句 'MCP works'，再用 add 算 999 加 1"),
]


def main() -> None:
    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        _log("Error: LLM_API_KEY environment variable is required")
        return

    llm = LLMClient(base_url=base_url, api_key=api_key, model=model)
    detail = DetailWriter(_OUTPUT_DIR)

    results: list[dict] = []
    pass_count = 0
    fail_count = 0

    # Build MCP-backed tool registry
    registry = ToolRegistry()
    mcp_config = MCPServerConfig(
        name="mock",
        command=[sys.executable, MOCK_SERVER_SCRIPT],
    )

    _log(f"\n{'='*60}")
    _log(f"  Phase 2.4 MCP Client Test  |  {len(test_cases)} cases")
    _log(f"  MCP server: {MOCK_SERVER_SCRIPT}")
    _log(f"  Detail logs -> {_OUTPUT_DIR}")
    _log(f"{'='*60}")

    with MCPToolRegistry(registry) as mcp_registry:
        # Start MCP server and register tools
        registered = mcp_registry.add_server(mcp_config)
        _log(f"\n  MCP tools registered: {registered}")
        assert "mock_echo" in registered, f"Expected mock_echo in {registered}"
        assert "mock_add" in registered, f"Expected mock_add in {registered}"
        _log("  Tool registration OK\n")

        # Create agent with the MCP-backed registry
        agent = Agent(
            llm=llm,
            tools=registry,
            memory=Memory(),
            budget=Budget(max_steps=10),
            strategy=FunctionCallingStrategy(),
        )

        for idx, (name, query) in enumerate(test_cases, 1):
            _log(f"[{idx}/{len(test_cases)}] {name}: {query}")
            t0 = time.time()
            detail.start_case(name, query)

            try:
                result = agent.run(query)
            except Exception as e:
                elapsed = time.time() - t0
                _log(f"  -> EXCEPTION ({elapsed:.1f}s): {e}")
                results.append({
                    "name": name, "ok": False, "steps": 0,
                    "answer": str(e), "elapsed": elapsed,
                })
                fail_count += 1
                continue

            elapsed = time.time() - t0
            s = result.trace.summary()
            ok = result.finished
            tag = "PASS" if ok else "FAIL"

            # Write detail to file
            for e in result.trace.events:
                detail.write_step(e)
            detail.finish_case(tag, s, elapsed, result.answer)

            # Console: one-line summary
            _log(f"  -> {tag}  |  {s['total_steps']} steps  |  {s['total_tokens']} tokens  |  {elapsed:.1f}s")

            results.append({
                "name": name, "ok": ok, "steps": s["total_steps"],
                "answer": _first_line(result.answer or ""),
                "elapsed": elapsed,
            })
            pass_count += int(ok)
            fail_count += int(not ok)

    # ── Summary ────────────────────────────────────────────────────
    _log(f"\n{'='*60}")
    _log(f"  RESULT: {pass_count} passed, {fail_count} failed  ({pass_count}/{len(test_cases)})")
    _log(f"  Detail logs -> {_OUTPUT_DIR}")
    _log(f"{'='*60}")

    for r in results:
        icon = "[PASS]" if r["ok"] else "[FAIL]"
        _log(f"  {icon} {r['name']:<20} {r['steps']} steps  {r['elapsed']:.1f}s")

    detail.write_summary(results, pass_count, fail_count)
    _log(f"\n  See detail logs: {_OUTPUT_DIR}/")
    _log("")
    llm.close()

    # Return exit code
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
