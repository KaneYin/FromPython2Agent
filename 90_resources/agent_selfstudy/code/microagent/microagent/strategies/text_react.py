"""TextReActStrategy — Phase 1 ReAct logic wrapped in strategy interface."""
from __future__ import annotations

from microagent.parser import parse
from microagent.prompts import build_system_prompt
from microagent.strategies.base import ParsedStep, ReasoningStrategy, ToolCall


class TextReActStrategy(ReasoningStrategy):
    name = "text_react"

    def __init__(self) -> None:
        self._system_prompt: str | None = None

    def build_request(self, memory, registry) -> tuple[list[dict], dict]:
        if self._system_prompt is None:
            self._system_prompt = build_system_prompt(registry)
        messages = [{"role": "system", "content": self._system_prompt}] + memory.to_messages()
        return messages, {"stop": ["Observation:"]}

    def parse_response(self, response) -> ParsedStep:
        parsed = parse(response.content)
        tool_calls = None
        if parsed.action and parsed.action_input:
            tool_calls = [ToolCall(
                call_id=None,
                name=parsed.action,
                arguments=parsed.action_input,
            )]
        return ParsedStep(
            thought=parsed.thought,
            is_final=parsed.is_final,
            final_answer=parsed.final_answer,
            tool_calls=tool_calls,
            parse_error=parsed.parse_error,
        )

    def format_assistant_message(self, response, parsed: ParsedStep) -> dict:
        return {"role": "assistant", "content": response.content}

    def format_observation_message(self, observation: str, tool_call: ToolCall) -> dict:
        return {"role": "user", "content": f"Observation: {observation}"}
