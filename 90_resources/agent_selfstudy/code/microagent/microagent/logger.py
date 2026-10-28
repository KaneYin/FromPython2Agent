"""Structured LLM I/O logger — writes JSONL for downstream visualization."""
from __future__ import annotations

import json
import time
from pathlib import Path


class LLMLogger:
    def __init__(self, log_dir: str = "logs", log_file: str = "llm_io.jsonl"):
        self._path = Path(log_dir) / log_file
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self._path

    def log_call(
        self,
        call_id: str,
        model: str,
        messages: list[dict],
        content: str,
        finish_reason: str | None,
        matched_stop: str | None,
        usage: dict,
        latency_ms: float,
        stop: list[str] | None = None,
        temperature: float = 0.0,
    ) -> None:
        entry = {
            "type": "llm_call",
            "call_id": call_id,
            "timestamp": time.time(),
            "time_str": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": model,
            "temperature": temperature,
            "stop": stop,
            "messages": messages,
            "content": content,
            "finish_reason": finish_reason,
            "matched_stop": matched_stop,
            "usage": usage,
            "latency_ms": round(latency_ms, 1),
        }
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_tool_call(
        self,
        tool_name: str,
        tool_input: dict,
        tool_output: str,
    ) -> None:
        entry = {
            "type": "tool_call",
            "timestamp": time.time(),
            "time_str": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output": tool_output,
        }
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    @staticmethod
    def list_log_files(log_dir: str = "logs") -> list[str]:
        p = Path(log_dir)
        if not p.exists():
            return []
        return sorted(f.name for f in p.glob("*.jsonl"))

    @staticmethod
    def read_log(file_path: str) -> list[dict]:
        entries = []
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries

    def clear(self) -> None:
        if self._path.exists():
            self._path.write_text("", encoding="utf-8")
