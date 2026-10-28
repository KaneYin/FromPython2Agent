from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict  # JSON Schema
    func: Callable[..., str]

    def invoke(self, **kwargs) -> str:
        try:
            return self.func(**kwargs)
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_all(self) -> list[Tool]:
        return list(self._tools.values())

    def render_for_prompt(self) -> str:
        parts: list[str] = []
        for tool in self._tools.values():
            parts.append(
                f"### {tool.name}\n"
                f"{tool.description}\n"
                f"Parameters: {json.dumps(tool.parameters, ensure_ascii=False, indent=2)}"
            )
        return "\n\n".join(parts)

    @property
    def tool_names(self) -> list[str]:
        return list(self._tools.keys())
