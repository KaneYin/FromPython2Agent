from langchain.agents import create_agent
from langchain_ollama import ChatOllama

"""
This is the minimal code that we can create a similar chatbot
that can interact with users. But as we can see in the tutorial, 
such bot heavily rely on the model, if we choose ollama, we 
have to install ollama relevant dependency to have our code runs.

So what should I do if we want to support multiple model providers
but do not need to code based on each mdoel provider's SDK or APIs?

THE ANSWER IS: ABSTRACTION
TODO: finish this notes part
"""

model = ChatOllama(
    model = "qwen3.5:9b",
    temperature = 0
)

agent = create_agent(
    model = model,
    tools = []
)

def main():
    messages = []
    while(True):
        content = input("What is your question?")
        if (content == "exit"):
            break
        messages.append({
            "role": "user",
            "content": content
        })

        responses = agent.invoke({
            "messages": messages
        })

        ai_response = responses["messages"][-1]
        print(ai_response.content)

if __name__ == "__main__":
    main()
