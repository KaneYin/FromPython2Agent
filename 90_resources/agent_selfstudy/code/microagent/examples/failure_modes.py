"""Failure modes systematic test — F1 through F10."""
from __future__ import annotations

import os

from microagent.agent import Agent
from microagent.budget import Budget
from microagent.llm import LLMCallRecord
from microagent.memory import Memory
from microagent.tools.base import Tool, ToolRegistry
from microagent.tools.calculator import calculator_tool


class ScriptedLLM:
    """Returns preset responses in sequence."""

    def __init__(self, responses: list[str]):
        self._responses = responses
        self._index = 0
        self._records: list[LLMCallRecord] = []

    def chat(self, messages, stop=None, temperature=0.0):
        if self._index < len(self._responses):
            content = self._responses[self._index]
            self._index += 1
        else:
            content = self._responses[-1]
        record = LLMCallRecord(
            call_id=f"f{self._index:04d}",
            timestamp=0.0,
            model="scripted",
            messages=messages,
            stop=stop,
            temperature=temperature,
            raw_response={},
            content=content,
            finish_reason="stop",
            matched_stop=None,
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            latency_ms=50.0,
        )
        self._records.append(record)
        return type("R", (), {"content": content, "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}, "latency_ms": 50.0})()

    def clear_records(self) -> None:
        self._records.clear()

    def get_records(self) -> list[LLMCallRecord]:
        return self._records


def _make_registry(*extra_tools: Tool) -> ToolRegistry:
    r = ToolRegistry()
    r.register(calculator_tool)
    for t in extra_tools:
        r.register(t)
    return r


def _run_case(label: str, agent: Agent, query: str) -> None:
    result = agent.run(query)
    print(f"\n{'='*60}")
    print(f"{label}: {query[:60]}...")
    print(f"{'='*60}")
    print(f"Finished: {result.finished} | Stop Reason: {result.stop_reason}")
    print(f"Answer: {result.answer}")
    used_tools = [e.content.get("action", "") for e in result.trace.events if e.type == "action"]
    print(f"Used Tools: {used_tools or '(none)'}")
    print(f"\n{result.trace.to_markdown()}")


def main() -> None:
    # F1: Tool name case mismatch
    print("\n" + "#"*60)
    print("# F1: Tool name case mismatch")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: I need to calculate\nAction: Calculator\nAction Input: {\"expression\": \"2+2\"}",
        "Thought: tool not found, let me retry with correct case\nAction: calculator\nAction Input: {\"expression\": \"2+2\"}",
        "Thought: got the result\nFinal Answer: 2+2=4",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F1", agent, "算一下 2+2")

    # F2: Action Input missing fields
    print("\n" + "#"*60)
    print("# F2: Action Input missing required fields")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: let me calculate\nAction: calculator\nAction Input: {}",
        "Thought: got error, let me provide expression\nAction: calculator\nAction Input: {\"expression\": \"5+5\"}",
        "Thought: done\nFinal Answer: 5+5=10",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F2", agent, "随便算一下")

    # F3: Action Input extra fields
    print("\n" + "#"*60)
    print("# F3: Action Input with extra fields")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: calculate with precision\nAction: calculator\nAction Input: {\"expression\": \"1+1\", \"precision\": 10}",
        "Thought: got result\nFinal Answer: 1+1=2, precision ignored by tool",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F3", agent, "计算 1+1，并指定精度为 10 位")

    # F4: Tool returns very long text
    print("\n" + "#"*60)
    print("# F4: Tool returns very long text")
    print("#"*60)
    long_tool = Tool(
        name="verbose_tool",
        description="A tool that returns very long output",
        parameters={"type": "object", "properties": {"n": {"type": "integer"}}, "required": ["n"]},
        func=lambda n: "x" * int(n),
    )
    llm = ScriptedLLM([
        "Thought: call verbose tool\nAction: verbose_tool\nAction Input: {\"n\": 5000}",
        "Thought: got long output\nFinal Answer: The tool returned 5000 characters",
    ])
    agent = Agent(llm=llm, tools=_make_registry(long_tool), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F4", agent, "调用一个返回很长的工具")

    # F5: Model computes directly without tool
    print("\n" + "#"*60)
    print("# F5: Model computes answer directly without tool")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: 2+2 is 4, no need for calculator\nFinal Answer: 2+2=4",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F5", agent, "算一下 2+2")

    # F6: Model outputs two Action blocks
    print("\n" + "#"*60)
    print("# F6: Model outputs two Action blocks")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: need two calcs\nAction: calculator\nAction Input: {\"expression\": \"1+1\"}\nThought: second calc\nAction: calculator\nAction Input: {\"expression\": \"2+2\"}",
        "Thought: got first result\nFinal Answer: Results: 1+1=2 and 2+2=4",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F6", agent, "先算 1+1 再算 2+2")

    # F7: Model output completely wrong format
    print("\n" + "#"*60)
    print("# F7: Model output completely wrong format")
    print("#"*60)
    llm = ScriptedLLM([
        "我觉得答案是 42",
        "Thought: I should follow format\nFinal Answer: The answer is 42",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F7", agent, "答案是什么")

    # F8: Tool keeps erroring
    print("\n" + "#"*60)
    print("# F8: Tool keeps returning errors")
    print("#"*60)
    broken_tool = Tool(
        name="broken",
        description="A tool that always fails",
        parameters={"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]},
        func=lambda x: (_ for _ in ()).throw(RuntimeError("always broken")),
    )
    llm = ScriptedLLM([
        "Thought: try broken tool\nAction: broken\nAction Input: {\"x\": \"test\"}",
        "Thought: error again, try once more\nAction: broken\nAction Input: {\"x\": \"test2\"}",
        "Thought: still broken, giving up\nFinal Answer: The tool is consistently failing, I cannot complete this task",
    ])
    agent = Agent(llm=llm, tools=_make_registry(broken_tool), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F8", agent, "用 broken 工具试试")

    # F9: Model hallucinates Observation
    print("\n" + "#"*60)
    print("# F9: Model hallucinates Observation (stop parameter test)")
    print("#"*60)
    llm = ScriptedLLM([
        "Thought: calculate\nAction: calculator\nAction Input: {\"expression\": \"3*3\"}\nObservation: 9\nFinal Answer: 3*3=9",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F9", agent, "算 3*3")

    # F10: Very long query (>2000 chars)
    print("\n" + "#"*60)
    print("# F10: Very long query")
    print("#"*60)
    long_query = "请帮我计算以下内容：" + "123 * 456 + " * 200 + "1 等于多少？"
    llm = ScriptedLLM([
        "Thought: this is a calculation request\nFinal Answer: The query is too long to process directly",
    ])
    agent = Agent(llm=llm, tools=_make_registry(), memory=Memory(), budget=Budget(max_steps=5))
    _run_case("F10", agent, long_query)


if __name__ == "__main__":
    main()
