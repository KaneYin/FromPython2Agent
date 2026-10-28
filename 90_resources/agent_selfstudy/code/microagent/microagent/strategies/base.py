"""ReasoningStrategy abstract base class and shared data types."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    call_id: str | None  # set by function calling; None for text ReAct
    name: str
    arguments: dict


@dataclass
class ParsedStep:
    thought: str | None
    is_final: bool
    final_answer: str | None = None
    tool_calls: list[ToolCall] | None = None
    parse_error: str | None = None


class ReasoningStrategy(ABC):
    name: str  # "text_react" / "function_call"

    @abstractmethod
    def build_request(
        self,
        memory,
        registry,
    ) -> tuple[list[dict], dict]:
        """Build LLM request. Returns (messages, extra_kwargs)."""

    @abstractmethod
    def parse_response(self, response) -> ParsedStep: ...

    @abstractmethod
    def format_assistant_message(self, response, parsed: ParsedStep) -> dict: ...

    @abstractmethod
    def format_observation_message(
        self,
        observation: str,
        tool_call: ToolCall,
    ) -> dict: ...
