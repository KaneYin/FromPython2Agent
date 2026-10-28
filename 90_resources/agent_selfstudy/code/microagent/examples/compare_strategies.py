"""Compare FunctionCalling vs TextReAct — 3 runs per query, stats + traces."""
from __future__ import annotations

import os
import statistics
from dataclasses import dataclass
from pathlib import Path

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.logger import LLMLogger
from microagent.memory import Memory
from microagent.strategies import FunctionCallingStrategy, TextReActStrategy
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool, str_tool
from microagent.tools.datetime_now import datetime_now_tool
from microagent.tools.text_stats import text_stats_tool
from dotenv import load_dotenv

load_dotenv()

RUNS = 3
TRACE_DIR = Path(__file__).parent / "traces"

QUERIES = [
    "你好",
    # "123 * 456 等于多少？",
    # "先算 12 * 8，再把结果加 100",
    # "现在几点？",
    # "帮我算 sqrt(-1)",
    # "统计'hello world'有几个单词，再告诉我现在时间",
    # "今天日期加上 365 天是哪天？",
]

STRATEGIES = [FunctionCallingStrategy, TextReActStrategy]


@dataclass
class RunResult:
    finished: bool
    steps: int
    total_tokens: int
    total_latency_ms: float
    answer: str | None
    trace_md: str


def _make_tools() -> ToolRegistry:
    registry = ToolRegistry()
    # registry.register(str_tool)
    registry.register(calculator_tool)
    registry.register(text_stats_tool)
    registry.register(datetime_now_tool)
    return registry


def _run_once(llm: LLMClient, strategy_cls, query: str, logger: LLMLogger | None = None) -> RunResult:
    agent = Agent(
        llm=llm,
        tools=_make_tools(),
        memory=Memory(),
        budget=Budget(max_steps=10),
        strategy=strategy_cls(),
    )
    result = agent.run(query)
    s = result.trace.summary()
    return RunResult(
        finished=result.finished,
        steps=s["total_steps"],
        total_tokens=s["total_tokens"],
        total_latency_ms=s["total_latency_ms"],
        answer=result.answer,
        trace_md=result.trace.to_markdown(),
    )


def _fmt_stat(values: list[int | float]) -> str:
    lo, hi = min(values), max(values)
    med = statistics.median(values)
    if lo == hi:
        return f"{lo}"
    return f"{med:.0f} (min={lo}, max={hi})"


def main() -> None:
    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        print("Error: LLM_API_KEY environment variable is required")
        return

    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    # header
    print(f"{'Query':40} | {'Strategy':20} | {'Done':4} | {'Steps':20} | {'Tokens':30} | {'Latency(ms)':30} | Answer")
    print("-" * 180)

    for qi, query in enumerate(QUERIES, 1):
        for strategy_cls in STRATEGIES:
            sname = strategy_cls.__name__
            runs: list[RunResult] = []
            for ri in range(RUNS):
                log_file = f"compare_q{qi}_{sname}_r{ri+1}.jsonl"
                logger = LLMLogger(log_dir="logs", log_file=log_file)
                llm = LLMClient(base_url=base_url, api_key=api_key, model=model, logger=logger)
                try:
                    r = _run_once(llm, strategy_cls, query)
                except Exception as e:
                    print(f"  ERROR: {e}")
                    llm.close()
                    continue
                runs.append(r)
                llm.close()

            if not runs:
                continue

            # Save first-run trace
            sname = strategy_cls.__name__
            trace_path = TRACE_DIR / f"q{qi}_{sname}.md"
            trace_path.write_text(runs[0].trace_md, encoding="utf-8")

            # Aggregate
            finished_all = all(r.finished for r in runs)
            tokens = [r.total_tokens for r in runs]
            latency = [r.total_latency_ms for r in runs]
            steps = [r.steps for r in runs]
            done_str = "Y" if finished_all else f"{sum(r.finished for r in runs)}/{RUNS}"
            answer_preview = (runs[0].answer or "N/A")[:60].replace("\n", " ")

            print(
                f"{query[:40]:40} | {sname:20} | {done_str:4} | "
                f"{_fmt_stat(steps):20} | {_fmt_stat(tokens):30} | "
                f"{_fmt_stat(latency):30} | {answer_preview}"
            )
        print()


if __name__ == "__main__":
    main()
