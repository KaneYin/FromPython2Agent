from typing import Protocol, Sequence

class ChatModel(Protocol):
    async def generate(
        self, 
        messages: Sequence[Message]
    ) -> ModelResponse:
        ...