import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, agent_middleware

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

@agent_middleware  # Explicitly marks as agent middleware
async def simple_agent_middleware(context, next):
    """Agent middleware with decorator - types are inferred."""
    print("Before agent execution")
    await next(context)
    print("After agent execution")


async def main():
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant.",
        middleware=[simple_agent_middleware],
    )
    # Run the agent
    result = await agent.run("Hello !")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
