from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from .logger import LLMLogger


@dataclass
class LLMCallRecord:
    call_id: str
    timestamp: float

    # Request
    model: str
    messages: list[dict]
    stop: list[str] | None
    temperature: float

    # Response
    raw_response: dict
    content: str
    finish_reason: str | None
    matched_stop: str | None
    usage: dict  # {prompt, completion, total}

    latency_ms: float


@dataclass
class LLMResponse:
    content: str
    usage: dict  # {prompt_tokens, completion_tokens, total_tokens}
    latency_ms: float
    raw_response: dict | None = None


class LLMError(Exception):
    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class LLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout: int = 60,
        logger: LLMLogger | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.logger = logger
        self._client = httpx.Client(timeout=timeout)
        self._call_records: list[LLMCallRecord] = []

    def get_records(self) -> list[LLMCallRecord]:
        return list(self._call_records)

    def clear_records(self) -> None:
        self._call_records.clear()

    def close(self) -> None:
        self._client.close()

    def __del__(self) -> None:
        try:
            self._client.close()
        except Exception:
            pass

    def chat(
        self,
        messages: list[dict],
        stop: list[str] | None = None,
        temperature: float = 0.0,
        **extra_kwargs,
    ) -> LLMResponse:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if stop:
            payload["stop"] = stop
        # Merge extra kwargs (tools, tool_choice, etc.)
        payload.update(extra_kwargs)

        start = time.monotonic()
        try:
            # print(payload)
            resp = self._client.post(url, json=payload, headers=headers)

        except httpx.RequestError as e:
            raise LLMError(f"Request failed: {e}") from e

        latency_ms = (time.monotonic() - start) * 1000

        if resp.status_code != 200:
            raise LLMError(
                f"API returned {resp.status_code}",
                status_code=resp.status_code,
                body=resp.text,
            )

        try:
            data = resp.json()
        except Exception as e:
            raise LLMError(f"Failed to parse response JSON: {e}", body=resp.text) from e

        try:
            content = data["choices"][0]["message"]["content"] or ""
            finish_reason = data["choices"][0].get("finish_reason")
            usage_raw = data.get("usage", {})
            usage = {
                "prompt_tokens": usage_raw.get("prompt_tokens", 0),
                "completion_tokens": usage_raw.get("completion_tokens", 0),
                "total_tokens": usage_raw.get("total_tokens", 0),
            }
        except (KeyError, IndexError) as e:
            raise LLMError(f"Unexpected response structure: {e}", body=resp.text) from e

        # Determine matched_stop
        matched_stop: str | None = None
        if finish_reason and "stop" in finish_reason.lower() and stop:
            for s in stop:
                if content.rstrip().endswith(s.rstrip()):
                    matched_stop = s
                    break

        # Record the call
        call_id = uuid.uuid4().hex[:8]
        record = LLMCallRecord(
            call_id=call_id,
            timestamp=time.time(),
            model=self.model,
            messages=messages,
            stop=stop,
            temperature=temperature,
            raw_response=data,
            content=content,
            finish_reason=finish_reason,
            matched_stop=matched_stop,
            usage=usage,
            latency_ms=latency_ms,
        )
        self._call_records.append(record)

        # Write to logger if configured
        if self.logger:
            self.logger.log_call(
                call_id=call_id,
                model=self.model,
                messages=messages,
                content=content,
                finish_reason=finish_reason,
                matched_stop=matched_stop,
                usage=usage,
                latency_ms=latency_ms,
                stop=stop,
                temperature=temperature,
            )

        return LLMResponse(content=content, usage=usage, latency_ms=latency_ms, raw_response=data)
