"""FunctionCallingStrategy — OpenAI tools API native function calling."""
from __future__ import annotations

import ast
import json

from microagent.strategies.base import ParsedStep, ReasoningStrategy, ToolCall

_FC_SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Use the provided tools when necessary."
)


class FunctionCallingStrategy(ReasoningStrategy):
    name = "function_call"

    def build_request(self, memory, registry) -> tuple[list[dict], dict]:
        messages = [{"role": "system", "content": _FC_SYSTEM_PROMPT}] + memory.to_messages()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in registry.list_all()
        ]
        return messages, {"tools": tools, "tool_choice": "auto"}

    def parse_response(self, response) -> ParsedStep:
        raw = response.raw_response
        msg = raw["choices"][0]["message"]
        tool_calls_raw = msg.get("tool_calls")
        content = msg.get("content")

        # Treat None and empty list both as "no tool calls"
        has_tool_calls = bool(tool_calls_raw)

        # Quirk 1: vLLM ignored tools param, model returned ReAct text
        if not has_tool_calls and content and "Action:" in content:
            return ParsedStep(
                thought=None,
                is_final=False,
                parse_error=(
                    "Model returned ReAct-style text output instead of tool_calls. "
                    "The backend may not support function calling. "
                    "Consider switching to TextReActStrategy."
                ),
            )

        # Normal final answer (no tool_calls or empty list)
        if not has_tool_calls:
            return ParsedStep(
                thought=None,
                is_final=True,
                final_answer=content or "",
            )

        # Parse tool_calls
        parsed_calls = []
        for tc in tool_calls_raw:
            args_str = tc["function"]["arguments"]
            try:
                args = json.loads(args_str)
            except json.JSONDecodeError:
                # Quirk 2: non-strict JSON from some models
                try:
                    args = ast.literal_eval(args_str)
                    if not isinstance(args, dict):
                        raise ValueError("args not a dict")
                except Exception as e:
                    return ParsedStep(
                        thought=content,
                        is_final=False,
                        parse_error=f"Cannot parse tool arguments: {args_str!r}, error: {e}",
                    )

            parsed_calls.append(ToolCall(
                call_id=tc.get("id"),
                name=tc["function"]["name"],
                arguments=args,
            ))

        # Quirk 3: content + tool_calls simultaneously — keep content as thought
        return ParsedStep(
            thought=content,
            is_final=False,
            tool_calls=parsed_calls,
        )

    def format_assistant_message(self, response, parsed: ParsedStep) -> dict:
        msg: dict = {"role": "assistant", "content": parsed.thought}
        if parsed.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.call_id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments, ensure_ascii=False),
                    },
                }
                for tc in parsed.tool_calls
            ]
        return msg

    def format_observation_message(self, observation: str, tool_call: ToolCall) -> dict:
        return {
            "role": "tool",
            "tool_call_id": tool_call.call_id,
            "content": observation,
        }
