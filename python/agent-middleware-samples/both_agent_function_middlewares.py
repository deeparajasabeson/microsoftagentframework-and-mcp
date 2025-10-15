import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import AgentRunContext, FunctionInvocationContext, ChatAgent

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# -----------------------------
# 🧠 Agent-level middleware
# -----------------------------
async def logging_agent_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    print("🌐 Agent starting a run...")
    await next(context)
    print("✅ Agent finished run!")

# -----------------------------
# ⚙️ Function-level middleware
# -----------------------------
async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    print(f"🔧 Calling function: {context.function.name}")
    await next(context)
    print(f"📦 Function result: {context.result}")


# -----------------------------
# 🛠️ Example tools (functions)
# -----------------------------
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"

async def get_time():
  """Get the current time."""
  from datetime import datetime
  return datetime.now().strftime("%H:%M:%S")

# -----------------------------
# 🤖 Create agent with middleware
# -----------------------------
async def main():
    agent = ChatAgent(
            chat_client=AzureOpenAIChatClient(
                api_key=api_key,
                endpoint=endpoint,
                deployment_name=deployment_name
        ),
        name="FriendlyAgent",
        tools=[get_time, say_hello],
        middleware=[logging_agent_middleware, logging_function_middleware],    # 👈 Agent-level
    )


    # -----------------------------
    # 🚀 Run the agent
    # -----------------------------
    result = await agent.run("Say hello to Deepa Steele with current time")

    print("\n💬 Agent response:")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())