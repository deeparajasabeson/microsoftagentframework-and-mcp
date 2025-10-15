 # Chat middleware intercepts chat requests sent to AI models.

import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import ChatAgent, ChatContext

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

async def logging_chat_middleware(
    context: ChatContext,
    next: Callable[[ChatContext], Awaitable[None]],
) -> None:
    """Chat middleware that logs AI interactions."""
    # Pre-processing: Log before AI call
    print(f"[Chat] Sending {len(context.messages)} messages to AI")

    # Continue to next middleware or AI service
    await next(context)

    # Post-processing: Log after AI response
    print("[Chat] AI response received")

async def main():
    print("Creating agent...")
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="ChatAgent",
        instructions="You are a Chat Agent.",
        middleware=[logging_chat_middleware],
    )
    # Run the agent
    print("Running agent...")

    userQuery = "Name all countries lie on Equator in a perfect aligned table.  Tropic of Capricorn or Tropic of Cancer which one pass through India ?"
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : {result.text}")

if __name__ == "__main__":
    asyncio.run(main())