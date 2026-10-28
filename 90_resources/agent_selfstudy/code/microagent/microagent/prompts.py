from __future__ import annotations

from microagent.tools.base import ToolRegistry

_SYSTEM_TEMPLATE = """
You are a helpful AI assistant that uses tools to answer questions.

You have access to the following tools:

{tool_descriptions}

Use the following format strictly:

Thought: your reasoning about what to do next
Action: the name of the tool to use, must be one of [{tool_names}]
Action Input: a single-line JSON object with the tool arguments

After you see the Observation, continue with another Thought/Action/Action Input cycle.

When you have enough information to answer, output:

Thought: your final reasoning
Final Answer: your answer to the user

Rules:
- Output ONE Thought + Action + Action Input per turn, then STOP and wait for Observation
- Action Input must be valid JSON on a single line
- If a tool returns an error, reason about it and try a different approach
- Do not fabricate Observations; they will be provided to you
"""


def build_system_prompt(registry: ToolRegistry) -> str:
    tool_descriptions = registry.render_for_prompt()
    tool_names = ", ".join(registry.tool_names)
    return _SYSTEM_TEMPLATE.format(
        tool_descriptions=tool_descriptions,
        tool_names=tool_names,
    )
