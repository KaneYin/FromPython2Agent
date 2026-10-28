from typing import Any, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

import ollama

class MyChatModel(BaseChatModel):
    model_name: str = "qwen3.5:9b"

    @property
    def _llm_type(self) -> str:
        return "my-ollama"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: List[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:

        ollama_messages = []

        for message in messages:
            ollama_messages.append({
                "role": self._convert_role,
                "content": message.content
            })
        
        ai_message = AIMessage(
            content=response["message"]["content"]
        )

        generation = ChatGeneration(
            message = ai_message
        )

        return ChatResult(
            generation=[generation]
        )
    
    def _convert_role(self, message: BaseMessage) -> str:
        if message.type == "human":
            return "user"
        if message.type == "ai":
            return "assistant"
        if message.type == "system":
            return "system"
        
        raise ValueError(f"Unsupported message type: {message.type}")

    