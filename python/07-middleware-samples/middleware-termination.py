import asyncio
from typing import Callable, Awaitable
from agent_framework import AgentRunContext     
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, agent_middleware

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

@agent_middleware  # Explicitly marks as agent middleware
async def blocking_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Middleware that blocks execution based on conditions."""
    # Check for blocked content
    last_message = context.messages[-1] if context.messages else None
    if last_message and last_message.text:
        if "blocked" in last_message.text.lower():
            print("Request blocked by middleware")
            context.terminate = True
            return

    # If no issues, continue normally
    await next(context)

async def main():
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant.",
        middleware=[blocking_middleware],
    )
    # Run the agent
    result = await agent.run("blocked content")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
