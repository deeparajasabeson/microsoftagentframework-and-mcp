""" Agent-Level vs Run-Level Middleware
Middleware can be registered at two levels with different scopes and behaviors.The one above is Agent-Level Middleware which is persistent across all runs, configured just once when creating the agent.

Run-Level Middleware Below is a way to have middleware just for specific run, allows per-request customization
 """    

import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import AgentRunContext, ChatAgent

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"


# --- Simple logging middleware ---
async def logging_agent_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Simple middleware that logs agent execution."""
    print("Agent starting...")

    # Continue to agent execution
    await next(context)

    print("Agent finished!")

async def main():
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant."
    )
    # Run the agent
    # Use middleware for this specific run only
    result = await agent.run(
        "This is important!",
        middleware=[logging_agent_middleware] # Run-level middleware (this run only)
    )
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
