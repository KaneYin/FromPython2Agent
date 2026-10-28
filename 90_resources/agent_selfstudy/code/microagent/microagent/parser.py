"""【中文导读】ReAct 文本协议的解析器。

ReAct 论文最原始的做法不是调 function calling API，而是让模型按固定文本格式输出：
    Thought: 我需要先算一下 …
    Action: calculator
    Action Input: {"expression": "2+3"}

这个文件的 parse() 就是用正则从模型输出里抠出这三段。注意几个工程细节：
- Final Answer 优先于 Action 检查：模型一旦给出最终答案就不再执行工具；
- 只取第一个 Action：避免模型一次输出多个动作导致失控；
- _extract_first_json_object：模型常在 JSON 后面跟"顺便说一句"之类的噪音，
  这里用括号配对只截出第一个完整 JSON 对象，容错性比 json.loads 整段解析高；
- 解析失败不抛异常，而是返回 parse_error —— 调用方（agent.py 的 h 步）
  会把错误喂回给模型，让它自我纠正。这是 ReAct 鲁棒性的关键一环。

对比：现代 function calling（OpenAI/Anthropic API 原生支持 tool_calls 结构化输出）
本质上是把这套"文本协议"做进了模型和 API 里，更可靠。这个仓库两种策略都
实现了（strategies/ 目录），建议对照着看。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass
class ParsedStep:
    thought: str
    is_final: bool
    final_answer: str | None = None
    action: str | None = None
    action_input: dict | None = None
    parse_error: str | None = None


_THOUGHT_RE = re.compile(r"Thought:\s*(.+?)(?=\n\s*(?:Action:|Final Answer:)|\Z)", re.DOTALL)
_FINAL_ANSWER_RE = re.compile(r"Final Answer:\s*(.+?)(?=\n\s*(?:Thought:|Action:)|\Z)", re.DOTALL)
_ACTION_RE = re.compile(r"Action:\s*(.+?)(?=\n\s*Action Input:|\Z)", re.DOTALL)
_ACTION_INPUT_RE = re.compile(r"Action Input:\s*(.+?)(?=\n\s*(?:Thought:|Action:|Final Answer:)|\Z)", re.DOTALL)


def _extract_first_json_object(s: str) -> str:
    """Extract the first complete JSON object {...} from a string, ignoring trailing noise."""
    depth = 0
    for i, ch in enumerate(s):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return s[:i + 1]
    return s


def parse(text: str) -> ParsedStep:
    # Extract thought (always required)
    thought_match = _THOUGHT_RE.search(text)
    thought = thought_match.group(1).strip() if thought_match else ""

    # Check Final Answer first (priority over Action)
    final_match = _FINAL_ANSWER_RE.search(text)
    if final_match:
        return ParsedStep(
            thought=thought,
            is_final=True,
            final_answer=final_match.group(1).strip(),
        )

    # Check Action
    action_matches = _ACTION_RE.findall(text)
    if not action_matches:
        return ParsedStep(
            thought=thought,
            is_final=False,
            parse_error="No Action or Final Answer found",
        )

    # Take the first Action only
    action = action_matches[0].strip()

    # Extract Action Input
    input_match = _ACTION_INPUT_RE.search(text)
    if not input_match:
        return ParsedStep(
            thought=thought,
            is_final=False,
            action=action,
            parse_error="No Action Input found",
        )

    raw_input = input_match.group(1).strip()
    # Strip trailing non-JSON noise (e.g. model-specific XML tool call tags)
    raw_input = _extract_first_json_object(raw_input)
    try:
        action_input = json.loads(raw_input)
    except json.JSONDecodeError as e:
        return ParsedStep(
            thought=thought,
            is_final=False,
            action=action,
            parse_error=f"Invalid JSON in Action Input: {e}",
        )

    if not isinstance(action_input, dict):
        return ParsedStep(
            thought=thought,
            is_final=False,
            action=action,
            parse_error="Action Input must be a JSON object",
        )

    return ParsedStep(
        thought=thought,
        is_final=False,
        action=action,
        action_input=action_input,
    )



if __name__ == "__main__":
    r = parse('Thought: need calc\nAction: calculator\nAction Input: {\"expression\": \"2+3\"}')
    print(r)