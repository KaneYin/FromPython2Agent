"""PlanExecuteStrategy — static Plan-and-Execute reasoning paradigm."""
from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass

from microagent.strategies.base import ParsedStep, ReasoningStrategy, ToolCall

_PLAN_SYSTEM_PROMPT = """\
You are a planning assistant. Given a user task and available tools, generate a step-by-step plan to accomplish the task.

Available tools:
{tool_descriptions}

Output format (strict):

Plan:
1. <one concrete action, mentioning which tool if applicable>
2. <next action>
3. ...

Rules:
- Each step must be a single concrete action
- If a step needs a tool, name the tool explicitly
- Plan must be linear (no branches, no conditionals)
- Maximum 8 steps
- The final step should produce the answer to the user
- Do not execute the plan, only generate it"""

_EXECUTE_SYSTEM_PROMPT = (
    "You are executing step {step_num} of a multi-step plan. "
    "Use the provided tool to accomplish this specific step. "
    "If the step doesn't need a tool, respond with the answer directly."
)


@dataclass
class PlanStep:
    index: int  # 1-indexed
    description: str
    completed: bool = False
    result: str | None = None


class PlanExecuteStrategy(ReasoningStrategy):
    name = "plan_execute"

    def __init__(self) -> None:
        self._plan: list[PlanStep] | None = None
        self._current_step_idx: int = 0
        self._plan_generated: bool = False
        self._user_query: str = ""

    def reset(self) -> None:
        self._plan = None
        self._current_step_idx = 0
        self._plan_generated = False
        self._user_query = ""

    # ------------------------------------------------------------------
    # build_request
    # ------------------------------------------------------------------
    def build_request(self, memory, registry) -> tuple[list[dict], dict]:
        if not self._plan_generated:
            # --- Plan phase ---
            msgs = memory.to_messages()
            if msgs and msgs[0].get("role") == "user":
                self._user_query = msgs[0]["content"]
            tool_descs = registry.render_for_prompt()
            messages = [
                {"role": "system", "content": _PLAN_SYSTEM_PROMPT.format(tool_descriptions=tool_descs)},
                {"role": "user", "content": self._user_query},
            ]
            return messages, {}

        # --- Execute phase ---
        # All steps done (last step had tool_calls) → ask for final summary
        if self._current_step_idx >= len(self._plan):
            return self._build_summary_request()

        current = self._plan[self._current_step_idx]
        system = _EXECUTE_SYSTEM_PROMPT.format(step_num=current.index)
        user = self._render_execute_prompt()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
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

    # ------------------------------------------------------------------
    # parse_response
    # ------------------------------------------------------------------
    def parse_response(self, response) -> ParsedStep:
        if not self._plan_generated:
            return self._parse_plan_phase(response)
        # All steps done — summary response is always final
        if self._plan is not None and self._current_step_idx >= len(self._plan):
            return ParsedStep(
                thought=response.content,
                is_final=True,
                final_answer=response.content or "",
            )
        return self._parse_execute_phase(response)

    # ------------------------------------------------------------------
    # format_assistant_message / format_observation_message
    # ------------------------------------------------------------------
    def format_assistant_message(self, response, parsed: ParsedStep) -> dict:
        if not self._plan_generated:
            return {"role": "assistant", "content": response.content}
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

    # ------------------------------------------------------------------
    # on_step_completed — called by Agent after tool execution
    # ------------------------------------------------------------------
    def on_step_completed(self, observations: list[str]) -> None:
        if not self._plan_generated or self._plan is None:
            return
        if self._current_step_idx < len(self._plan):
            self._plan[self._current_step_idx].completed = True
            self._plan[self._current_step_idx].result = "\n".join(observations)
            self._current_step_idx += 1

    # ------------------------------------------------------------------
    # Properties for trace rendering
    # ------------------------------------------------------------------
    @property
    def plan_phase(self) -> str:
        return "executing" if self._plan_generated else "planning"

    @property
    def plan_steps(self) -> list[PlanStep] | None:
        return self._plan

    @property
    def current_step_info(self) -> tuple[int, int] | None:
        if self._plan is None:
            return None
        return (self._current_step_idx + 1, len(self._plan))

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _parse_plan(self, text: str) -> list[PlanStep]:
        steps: list[PlanStep] = []
        for m in re.finditer(r"^\d+\.\s+(.+)$", text, re.MULTILINE):
            steps.append(PlanStep(index=len(steps) + 1, description=m.group(1).strip()))
        return steps

    def _parse_plan_phase(self, response) -> ParsedStep:
        plan_steps = self._parse_plan(response.content or "")
        if not plan_steps:
            return ParsedStep(
                thought=None,
                is_final=False,
                parse_error="Failed to parse plan from LLM output",
            )

        self._plan = plan_steps
        self._plan_generated = True

        return ParsedStep(
            thought=f"Generated plan with {len(plan_steps)} steps",
            is_final=False,
            tool_calls=[],
        )

    def _parse_execute_phase(self, response) -> ParsedStep:
        raw = response.raw_response
        msg = raw["choices"][0]["message"]
        tool_calls_raw = msg.get("tool_calls")
        content = msg.get("content")
        has_tool_calls = bool(tool_calls_raw)

        if not has_tool_calls:
            is_last = self._current_step_idx >= len(self._plan) - 1 if self._plan else True
            if is_last:
                return ParsedStep(
                    thought=content,
                    is_final=True,
                    final_answer=content or "",
                )
            return ParsedStep(
                thought=content,
                is_final=False,
                tool_calls=[],
            )

        parsed_calls = []
        for tc in tool_calls_raw:
            args_str = tc["function"]["arguments"]
            try:
                args = json.loads(args_str)
            except json.JSONDecodeError:
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

        return ParsedStep(
            thought=content,
            is_final=False,
            tool_calls=parsed_calls,
        )

    def _render_execute_prompt(self) -> str:
        assert self._plan is not None
        lines = [f"Original task: {self._user_query}\n"]
        lines.append("Full plan:")
        for step in self._plan:
            marker = ""
            if step.completed:
                marker = f" [completed: result={step.result}]"
            elif step.index - 1 == self._current_step_idx:
                marker = " ← CURRENT STEP"
            lines.append(f"{step.index}. {step.description}{marker}")
        lines.append(f"\nExecute step {self._current_step_idx + 1} only.")
        return "\n".join(lines)

    def _build_summary_request(self) -> tuple[list[dict], dict]:
        assert self._plan is not None
        lines = [
            "All plan steps have been executed. Here are the results:\n",
            f"Original task: {self._user_query}\n",
        ]
        for step in self._plan:
            lines.append(f"{step.index}. {step.description} → {step.result}")
        lines.append("\nBased on the above results, provide the final answer to the user.")
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Summarize the results and answer the user's question."},
            {"role": "user", "content": "\n".join(lines)},
        ]
        return messages, {}
