from litellm import acompletion

class LiteLLMModel:
    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
    ):
        self.model = model
        self.temperature = temperature
    
    async def generate(
        self,
        messages: list[Message],
    ) -> ModelResponse:

        response = await acompletion(
            model=self.model,
            messages=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            temperature = self.temperature,
        )

        choice = response.choices[0]

        return ModelResponse(
            content = choice.message.content or "",
            finish_reason = choise.finish_reason,
            usage = Usage(
                input_tokens = response.usage.prompt_tokens,
                output_tokens = response.usage.completion_tokens,
            ),
        )

        