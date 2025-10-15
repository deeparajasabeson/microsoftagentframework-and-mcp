import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import ChatAgent, FunctionMiddleware, FunctionInvocationContext

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# -----------------------------------------------------
# 🧠 Middleware Definition
# -----------------------------------------------------
class LoggingFunctionMiddleware(FunctionMiddleware):
    """Function middleware that logs function execution."""

    async def process(
        self,
        context: FunctionInvocationContext,
        next: Callable[[FunctionInvocationContext], Awaitable[None]],
    ) -> None:
        # Pre-processing: Log before function execution
        print(f"🟡 [Function Class] [Before] Calling {context.function.name}")
        print(f"📥 Arguments: {context.arguments}")

        # Continue to next middleware or function execution
        await next(context)

        # Post-processing: Log after function execution
        print(f"🟢 [Function Class] [After] Function completed: {context.function.name}")
        print(f"📤 Result: {context.result}")

# -----------------------------------------------------
# 🧠 Creating 2 Functions for Tools
# -----------------------------------------------------
# 1️⃣ Define sample tools (functions)
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"

async def get_time() -> str:
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        name="GeographyAgent",
        instructions="You are a Geography Agent.",
        tools=[get_time, say_hello],
        middleware=[LoggingFunctionMiddleware()], # <-- Attach class-based middleware with ()
    )
    # Run the agent
    print("Running agent...")

    userQuery = "Name countries/territories in Australia in a lined perfect aligned table (lines on all sides including heading) with more than 3 columns of your choice with listing each country in a separate row.  Say hello to Deepa and tell the current time at Atlanta."
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : \n{result.text}")

if __name__ == "__main__":
    asyncio.run(main())