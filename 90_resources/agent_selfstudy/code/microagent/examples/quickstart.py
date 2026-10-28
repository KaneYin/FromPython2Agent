"""MicroAgent quickstart — compare Function Calling vs Text ReAct."""
from __future__ import annotations

import os

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.logger import LLMLogger
from microagent.memory import Memory
from microagent.strategies import FunctionCallingStrategy, TextReActStrategy
from microagent.tools.base import ToolRegistry
from microagent.tools.bash import bash_tool
from microagent.tools.calculator import calculator_tool
from microagent.tools.datetime_now import datetime_now_tool
from microagent.tools.file_io import file_read_tool, file_write_tool
from microagent.tools.text_stats import text_stats_tool
from microagent.tools.web_search import web_search_tool
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        print("Error: LLM_API_KEY environment variable is required")
        return

    queries = [
        "你好，介绍一下你自己",
        "123 * 456 等于多少？",
        "先算 12 * 8，再把结果加 100",
    ]

    for strategy_cls in [FunctionCallingStrategy, TextReActStrategy]:
        print(f"\n{'='*60}")
        print(f"Strategy: {strategy_cls.__name__}")
        print(f"{'='*60}")

        logger = LLMLogger(log_dir="logs", log_file=f"{strategy_cls.__name__}.jsonl")
        llm = LLMClient(base_url=base_url, api_key=api_key, model=model, logger=logger)
        registry = ToolRegistry()
        registry.register(calculator_tool)
        registry.register(text_stats_tool)
        registry.register(datetime_now_tool)
        registry.register(bash_tool)
        registry.register(file_read_tool)
        registry.register(file_write_tool)
        # web_search only if API key is available
        if os.environ.get("TAVILY_API_KEY"):
            registry.register(web_search_tool)
        else:
            print("  [hint] TAVILY_API_KEY not set, skipping web_search tool")

        agent = Agent(
            llm=llm, tools=registry, memory=Memory(),
            budget=Budget(max_steps=10), strategy=strategy_cls(),
        )

        for i, query in enumerate(queries, 1):
            print(f"\n--- Query {i}: {query} ---")
            result = agent.run(query)
            print(f"Finished: {result.finished} | Stop: {result.stop_reason}")
            print(f"Answer: {result.answer}")
            s = result.trace.summary()
            print(f"Steps: {s['total_steps']} | Tokens: {s['total_tokens']} | Latency: {s['total_latency_ms']}ms")

        llm.close()


if __name__ == "__main__":
    main()
