from __future__ import annotations


class Memory:
    def __init__(self) -> None:
        self._messages: list[dict] = []

    def add_user(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str) -> None:
        self._messages.append({"role": "assistant", "content": text})

    def add_observation(self, text: str) -> None:
        self._messages.append({"role": "user", "content": f"Observation: {text}"})

    def add_raw(self, message: dict) -> None:
        self._messages.append(message)

    def to_messages(self) -> list[dict]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()
