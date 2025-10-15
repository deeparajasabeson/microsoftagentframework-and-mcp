import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import ChatAgent, ChatMiddleware, ChatContext

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# -----------------------------------------------------
# 🧠 Middleware Definition
# -----------------------------------------------------
class LoggingChatMiddleware(ChatMiddleware):
    """Chat middleware that logs execution."""

    async def process(
        self,
        context: ChatContext,
        next: Callable[[ChatMiddleware], Awaitable[None]],
    ) -> None:
        # Pre-processing: Log before AI call
        print(f"[Chat Class] Sending {len(context.messages)} messages to AI")

        # Continue to next middleware or AI service
        await next(context)

        # Post-processing: Log after AI response
        print("[Chat Class] AI response received")

# -----------------------------------------------------
# 🧠 Creating and Run Agent
# -----------------------------------------------------
async def main():
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="FunnyAgent",
        instructions="You are a Funny and Polite Chat Agent.",
        middleware=[LoggingChatMiddleware()], # <-- Attach class-based middleware with ()
    )
    # Run the agent
    print("Running agent...")

    userQuery = "Tell few jokes on various topics and genre..."
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : \n{result.text}")

if __name__ == "__main__":
    asyncio.run(main())