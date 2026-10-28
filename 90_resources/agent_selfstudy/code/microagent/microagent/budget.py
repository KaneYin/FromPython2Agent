from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Budget:
    max_steps: int = 10
    max_total_tokens: int | None = None

    _steps_used: int = field(default=0, repr=False)
    _tokens_used: int = field(default=0, repr=False)

    def consume_step(self) -> None:
        self._steps_used += 1

    def consume_tokens(self, n: int) -> None:
        self._tokens_used += n

    def exceeded(self) -> tuple[bool, str | None]:
        if self._steps_used >= self.max_steps:
            return True, f"max_steps ({self.max_steps}) reached"
        if self.max_total_tokens is not None and self._tokens_used >= self.max_total_tokens:
            return True, f"max_total_tokens ({self.max_total_tokens}) reached"
        return False, None
