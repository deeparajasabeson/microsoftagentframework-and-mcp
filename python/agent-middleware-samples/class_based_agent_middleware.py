import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable
from agent_framework import ChatAgent, AgentMiddleware, AgentRunContext

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# -----------------------------------------------------
# 🧠 Middleware Definition
# -----------------------------------------------------
class LoggingAgentMiddleware(AgentMiddleware):
    """Agent middleware that logs execution."""

    async def process(
        self,
        context: AgentRunContext,
        next: Callable[[AgentRunContext], Awaitable[None]],
    ) -> None:
        # Pre-processing: Log before agent execution
        print("[Agent Class] Starting execution")

        # Continue to next middleware or agent execution
        await next(context)

        # Post-processing: Log after agent execution
        print("[Agent Class] Execution completed")

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
        name="ChatAgent",
        instructions="You are a Chat Agent.",
        middleware=[LoggingAgentMiddleware()], # <-- Attach class-based middleware with ()
    )
    # Run the agent
    print("Running agent...")

    userQuery = "Name countries in South America in a lined perfect aligned table with more than 3 columns of your choice with listing each country in a separate row."
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : \n{result.text}")
    
if __name__ == "__main__":
    asyncio.run(main()) 