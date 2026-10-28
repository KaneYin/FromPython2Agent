"""Edge case verification — run two cases and print traces."""
from __future__ import annotations

import os

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMClient
from microagent.memory import Memory
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool


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


def main() -> None:
    load_dotenv()

    base_url = os.environ.get("LLM_BASE_URL", "")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")

    if not api_key:
        print("Error: LLM_API_KEY not set. Check .env file or environment variables.")
        return

    llm = LLMClient(base_url=base_url, api_key=api_key, model=model)

    # --- Case A: Error Recovery (sqrt of negative number) ---
    print("=" * 60)
    print("Case A: sqrt(-1) error recovery")
    print("=" * 60 + "\n")

    registry_a = ToolRegistry()
    registry_a.register(calculator_tool)
    agent_a = Agent(llm=llm, tools=registry_a, memory=Memory(), budget=Budget(max_steps=10))
    result_a = agent_a.run("帮我算 sqrt(-1)，告诉我结果")

    print(f"Finished: {result_a.finished}")
    print(f"Stop Reason: {result_a.stop_reason}")
    print(f"Answer: {result_a.answer}\n")
    print(result_a.trace.to_markdown())

    # --- Case B: max_steps graceful stop ---
    print("=" * 60)
    print("Case B: max_steps=2 graceful stop")
    print("=" * 60 + "\n")

    registry_b = ToolRegistry()
    registry_b.register(calculator_tool)
    agent_b = Agent(
        llm=llm, tools=registry_b, memory=Memory(),
        budget=Budget(max_steps=2),
    )
    result_b = agent_b.run("先算 5+5，再算结果乘 2，再算结果减 3，再算结果除以 2")

    print(f"Finished: {result_b.finished}")
    print(f"Stop Reason: {result_b.stop_reason}")
    print(f"Answer: {result_b.answer}\n")
    print(result_b.trace.to_markdown())

    # Verify
    assert not result_b.finished, "Case B should not finish"
    assert result_b.stop_reason == "max_steps", f"Expected 'max_steps', got '{result_b.stop_reason}'"
    print("Case B assertion passed: finished=False, stop_reason=max_steps")


if __name__ == "__main__":
    main()
