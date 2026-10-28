"""Tool selection test — 6 queries to exercise multi-tool behavior."""
from __future__ import annotations

import os

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.memory import Memory
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool
from microagent.tools.datetime_now import datetime_now_tool
from microagent.tools.text_stats import text_stats_tool


def load_dotenv() -> None:
    from pathlib import Path
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value


def _extract_used_tools(trace) -> list[str]:
    tools = []
    for e in trace.events:
        if e.type == "action":
            tools.append(e.content.get("action", ""))
    return tools


def main() -> None:
    load_dotenv()

    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        print("Error: LLM_API_KEY not set. Check .env file or environment variables.")
        return

    llm = LLMClient(base_url=base_url, api_key=api_key, model=model)
    registry = ToolRegistry()
    # registry.register(calculator_tool)
    # registry.register(text_stats_tool)
    # registry.register(datetime_now_tool)
    agent = Agent(llm=llm, tools=registry, memory=Memory(), budget=Budget(max_steps=10))

    queries = [
        "你好啊",
        # "帮我算 sqrt(2) 的近似值",
        # "统计这段话的字数：'人工智能正在改变世界'",
        # "今天日期加上 365 等于多少？",
        # "我想知道'hello world'有几个单词，再告诉我现在的时间",
        # "你好",
    ]

    print(f"{'='*70}")
    print(f"{'Query':<6} | {'Finished':<8} | {'Stop Reason':<14} | {'Steps':<5} | {'Used Tools'}")
    print(f"{'='*70}")

    for i, query in enumerate(queries, 1):
        result = agent.run(query)
        used_tools = _extract_used_tools(result.trace)
        step_count = max((e.step for e in result.trace.events), default=0)
        tools_str = ", ".join(used_tools) if used_tools else "(none)"

        print(f"{i:<6} | {str(result.finished):<8} | {result.stop_reason:<14} | {step_count:<5} | {tools_str}")

    print(f"{'='*70}")

    # Print full traces for review
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print(f"{'='*60}\n")
        # Re-run for trace output (agent resets memory each run)
        result = agent.run(query)
        print(result.trace.to_markdown())


if __name__ == "__main__":
    main()
