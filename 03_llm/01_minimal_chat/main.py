import asyncio

from model.base import ChatModel
from model.litellm_model import LiteLLMModel
from model.types import Message


async def chat(model: ChatModel):
    messages: list[Message] = []

    while True:
        user_input = input("You: ")

        if user_input == "exit":
            break

        messages.append(
            Message(
                role="user",
                content=user_input,
            )
        )

        response = await model.generate(messages)

        messages.append(
            Message(
                role="assistant",
                content=response.content,
            )
        )

        print("Assistant:", response.content)


async def main():
    model = LiteLLMModel(
        model="openai/gpt-4o-mini"
    )

    await chat(model)


if __name__ == "__main__":
    asyncio.run(main())