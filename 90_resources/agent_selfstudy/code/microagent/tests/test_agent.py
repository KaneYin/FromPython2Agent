from __future__ import annotations

from dataclasses import dataclass

from microagent.agent import Agent, AgentResult
from microagent.budget import Budget
from microagent.llm import LLMCallRecord, LLMClient, LLMResponse
from microagent.memory import Memory
from microagent.strategies import TextReActStrategy
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool


@dataclass
class MockResponse:
    content: str
    usage: dict
    latency_ms: float = 100.0
    raw_response: dict | None = None


class MockLLM:
    """Returns preset responses in sequence, looping the last one."""

    def __init__(self, responses: list[MockResponse]):
        self.responses = responses
        self._index = 0
        self._records: list = []

    def chat(self, messages, stop=None, temperature=0.0, **extra_kwargs):
        if self._index < len(self.responses):
            resp = self.responses[self._index]
            self._index += 1
        else:
            resp = self.responses[-1]
        # Build raw_response if not provided (for text ReAct tests)
        raw = resp.raw_response or {
            "choices": [{"message": {"content": resp.content}, "finish_reason": "stop"}],
        }
        record = LLMCallRecord(
            call_id=f"mock{self._index:04d}",
            timestamp=0.0,
            model="mock",
            messages=messages,
            stop=stop,
            temperature=temperature,
            raw_response=raw,
            content=resp.content,
            finish_reason="stop",
            matched_stop=None,
            usage=resp.usage,
            latency_ms=resp.latency_ms,
        )
        self._records.append(record)
        # Return LLMResponse with raw_response
        return LLMResponse(
            content=resp.content,
            usage=resp.usage,
            latency_ms=resp.latency_ms,
            raw_response=raw,
        )

    def clear_records(self) -> None:
        self._records.clear()

    def get_records(self) -> list:
        return self._records


def _make_agent(mock_llm, budget=None):
    registry = ToolRegistry()
    registry.register(calculator_tool)
    return Agent(
        llm=mock_llm,  # type: ignore
        tools=registry,
        memory=Memory(),
        budget=budget or Budget(max_steps=10),
        strategy=TextReActStrategy(),
    )


class TestDirectFinalAnswer:
    def test_single_step_answer(self):
        llm = MockLLM([
            MockResponse(
                content="Thought: I can answer directly\nFinal Answer: Hello!",
                usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            ),
        ])
        agent = _make_agent(llm)
        result = agent.run("你好")
        assert result.finished is True
        assert result.answer == "Hello!"
        assert result.stop_reason == "final_answer"
        assert len(result.trace.events) >= 1


class TestTwoStepToolCall:
    def test_tool_then_answer(self):
        llm = MockLLM([
            MockResponse(
                content="Thought: need to calculate\nAction: calculator\nAction Input: {\"expression\": \"12 * 8\"}",
                usage={"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
            ),
            MockResponse(
                content="Thought: got the result, now add 100\nFinal Answer: 196",
                usage={"prompt_tokens": 80, "completion_tokens": 15, "total_tokens": 95},
            ),
        ])
        agent = _make_agent(llm)
        result = agent.run("先算 12 * 8，再把结果加 100")
        assert result.finished is True
        assert result.answer == "196"
        # should have: think(step1) + action(step1) + observation(step1) + think/final(step2)
        types = [e.type for e in result.trace.events]
        assert "action" in types
        assert "observation" in types
        assert "final" in types


class TestToolErrorRetry:
    def test_tool_error_then_success(self):
        registry = ToolRegistry()
        call_count = 0

        def _flaky_tool(x: str) -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return "Error: ValueError: something went wrong"
            return "42"

        from microagent.tools.base import Tool
        registry.register(Tool(
            name="flaky",
            description="a flaky tool",
            parameters={"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]},
            func=_flaky_tool,
        ))

        llm = MockLLM([
            MockResponse(
                content="Thought: try flaky\nAction: flaky\nAction Input: {\"x\": \"test\"}",
                usage={"prompt_tokens": 30, "completion_tokens": 10, "total_tokens": 40},
            ),
            MockResponse(
                content="Thought: tool errored, let me answer\nFinal Answer: The answer is 42",
                usage={"prompt_tokens": 60, "completion_tokens": 15, "total_tokens": 75},
            ),
        ])
        agent = Agent(llm=llm, tools=registry, memory=Memory(), budget=Budget(max_steps=10), strategy=TextReActStrategy())
        result = agent.run("use the flaky tool")
        assert result.finished is True
        assert "42" in result.answer


class TestParseErrorRetry:
    def test_parse_error_then_correct(self):
        llm = MockLLM([
            MockResponse(
                content="Thought: I'll do something\nJust some garbled output without proper format",
                usage={"prompt_tokens": 30, "completion_tokens": 10, "total_tokens": 40},
            ),
            MockResponse(
                content="Thought: I should follow format\nFinal Answer: Corrected answer",
                usage={"prompt_tokens": 60, "completion_tokens": 10, "total_tokens": 70},
            ),
        ])
        agent = _make_agent(llm)
        result = agent.run("test parse error recovery")
        assert result.finished is True
        assert result.answer == "Corrected answer"
        # should have an observation event with the parse error feedback
        types = [e.type for e in result.trace.events]
        assert "observation" in types


class TestMaxSteps:
    def test_max_steps_exits_gracefully(self):
        # Every response is a tool call, never reaches Final Answer
        response = MockResponse(
            content="Thought: keep going\nAction: calculator\nAction Input: {\"expression\": \"1+1\"}",
            usage={"prompt_tokens": 30, "completion_tokens": 10, "total_tokens": 40},
        )
        llm = MockLLM([response])
        agent = _make_agent(llm, budget=Budget(max_steps=2))
        result = agent.run("keep calculating")
        assert result.finished is False
        assert result.stop_reason == "max_steps"
        assert result.answer is None


class TestFunctionCalling:
    def test_fc_tool_then_answer(self):
        from microagent.strategies import FunctionCallingStrategy
        # First response: tool call
        raw1 = {
            "choices": [{"message": {
                "content": None,
                "tool_calls": [{"id": "call_001", "type": "function", "function": {
                    "name": "calculator", "arguments": '{"expression": "12 * 8"}',
                }}],
            }, "finish_reason": "tool_calls"}],
        }
        # Second response: final answer
        raw2 = {
            "choices": [{"message": {"content": "196", "tool_calls": None}, "finish_reason": "stop"}],
        }
        llm = MockLLM([
            MockResponse(
                content="", usage={"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
                raw_response=raw1,
            ),
            MockResponse(
                content="196", usage={"prompt_tokens": 80, "completion_tokens": 10, "total_tokens": 90},
                raw_response=raw2,
            ),
        ])
        agent = Agent(
            llm=llm, tools=ToolRegistry(), memory=Memory(),
            budget=Budget(max_steps=10), strategy=FunctionCallingStrategy(),
        )
        agent.tools.register(calculator_tool)
        result = agent.run("先算 12 * 8，再把结果加 100")
        assert result.finished is True
        assert result.answer == "196"
        # trace should have strategy_name
        think_events = [e for e in result.trace.events if e.type == "think"]
        assert all(e.strategy_name == "function_call" for e in think_events)

    def test_fc_final_answer_directly(self):
        from microagent.strategies import FunctionCallingStrategy
        raw = {
            "choices": [{"message": {"content": "Hello!", "tool_calls": None}, "finish_reason": "stop"}],
        }
        llm = MockLLM([
            MockResponse(
                content="Hello!", usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
                raw_response=raw,
            ),
        ])
        agent = Agent(
            llm=llm, tools=ToolRegistry(), memory=Memory(),
            budget=Budget(max_steps=10), strategy=FunctionCallingStrategy(),
        )
        result = agent.run("你好")
        assert result.finished is True
        assert result.answer == "Hello!"

    def test_text_react_strategy_in_trace(self):
        llm = MockLLM([
            MockResponse(
                content="Thought: I can answer\nFinal Answer: 42",
                usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            ),
        ])
        agent = _make_agent(llm)
        result = agent.run("test")
        think_events = [e for e in result.trace.events if e.type == "think"]
        assert all(e.strategy_name == "text_react" for e in think_events)
