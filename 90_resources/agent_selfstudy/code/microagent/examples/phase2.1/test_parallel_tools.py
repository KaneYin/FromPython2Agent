"""Phase 2.1 validation: parallel tool calling support.

Q6: "统计'hello world'有几个单词，再告诉我现在时间"
Expect: 1 step with 2 tool_calls executed, vs Phase 1.5's 2 steps (1 tool_call dropped).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.logger import LLMLogger
from microagent.memory import Memory
from microagent.strategies import FunctionCallingStrategy
from microagent.tools.base import ToolRegistry
from microagent.tools.datetime_now import datetime_now_tool
from microagent.tools.text_stats import text_stats_tool

load_dotenv()

RUNS = 3
TRACE_DIR = Path(__file__).parent / "traces"
QUERY = "统计'hello world'有几个单词，再告诉我现在时间"


def _make_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(text_stats_tool)
    registry.register(datetime_now_tool)
    return registry


def _count_tool_actions(trace_md: str, step: int) -> int:
    """Count action events in a specific step from trace markdown."""
    count = 0
    for line in trace_md.splitlines():
        if f"Step {step} — action" in line:
            count += 1
    return count


def main() -> None:
    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        print("Error: LLM_API_KEY environment variable is required")
        return

    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Phase 2.1 — Parallel Tool Calling Validation")
    print(f"Query: {QUERY}")
    print(f"Runs: {RUNS}\n")

    header = f"{'Run':>4} | {'Steps':>5} | {'Tokens':>7} | {'Actions':>7} | {'Done':>4} | Answer"
    print(header)
    print("-" * len(header))

    for ri in range(RUNS):
        log_file = f"parallel_q6_r{ri + 1}.jsonl"
        logger = LLMLogger(log_dir="logs", log_file=log_file)
        llm = LLMClient(base_url=base_url, api_key=api_key, model=model, logger=logger)

        agent = Agent(
            llm=llm,
            tools=_make_tools(),
            memory=Memory(),
            budget=Budget(max_steps=10),
            strategy=FunctionCallingStrategy(),
        )
        result = agent.run(QUERY)
        s = result.trace.summary()
        llm.close()

        # Count tool actions in step 1
        trace_md = result.trace.to_markdown()
        actions = _count_tool_actions(trace_md, 1)
        done = "Y" if result.finished else "N"
        answer_preview = (result.answer or "N/A")[:60].replace("\n", " ")

        print(
            f"{ri + 1:4} | {s['total_steps']:5} | {s['total_tokens']:7} | "
            f"{actions:7} | {done:4} | {answer_preview}"
        )

        # Save trace
        trace_path = TRACE_DIR / f"q6_parallel_r{ri + 1}.md"
        trace_path.write_text(trace_md, encoding="utf-8")

    print()
    print("--- Phase 1.5 vs Phase 2.1 Expected Comparison ---")
    print(f"{'Metric':30} | {'Phase 1.5':20} | {'Phase 2.1 Expected':20}")
    print("-" * 75)
    print(f"{'Steps':30} | {'2':20} | {'1':20}")
    print(f"{'Tool calls executed':30} | {'1 (dropped 1)':20} | {'2 (all executed)':20}")
    print(f"{'Final answer correctness':30} | {'Correct':20} | {'Correct':20}")
    print()
    print("Note: If steps didn't drop from 2 to 1, the model may not have")
    print("returned parallel tool_calls — this is a model behavior difference, not a bug.")
    print("Check the saved traces in examples/phase2.1/traces/ for details.")


if __name__ == "__main__":
    main()
