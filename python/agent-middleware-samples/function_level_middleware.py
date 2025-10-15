import asyncio
from agent_framework import FunctionInvocationContext, ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

def get_time():
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """Middleware that logs function calls."""
    print(f"Calling function: {context.function.name}")

    await next(context)

    print(f"Function result: {context.result}")
    
async def main():
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="TimeAgent",
        instructions="You can tell the current time.",
        tools=[get_time],
        middleware=[logging_function_middleware],
    )
    # Run the agent
    print("Running agent...")

    userQuery = "What time is it?"
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : {result.text}")


if __name__ == "__main__":
    asyncio.run(main())