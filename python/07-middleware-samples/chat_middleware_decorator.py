import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, chat_middleware

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

@chat_middleware  # Explicitly marks as chat middleware
async def simple_chat_middleware(context, next):
    """Chat middleware with decorator - types are inferred."""
    print(f"Processing {len(context.messages)} chat messages")
    await next(context)
    print("Chat processing completed")

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
        middleware=[simple_chat_middleware],
    )
    # Run the agent
    print("Running agent...")

    userQuery = "Name all countries lie on Tropic of Capricorn in a lined perfect aligned table with enought columns of your choice."
    result = await agent.run(userQuery)

    print(f"User Query : {userQuery}")
    print(f"Agent Response : {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
