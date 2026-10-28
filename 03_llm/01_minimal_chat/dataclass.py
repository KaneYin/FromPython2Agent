from dataclass import dataclass
from typing import Literal

Role = Literal["system", "user", "assistant"]

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

@dataclass
class ModelResponse:
    content: str
    finish_reason: str | None = None
    usage: Usage | None = None

