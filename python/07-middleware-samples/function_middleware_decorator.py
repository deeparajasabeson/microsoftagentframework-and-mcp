import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, function_middleware

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"


@function_middleware  # Explicitly marks as function middleware
async def simple_function_middleware(context, next):
    """Function middleware with decorator - types are inferred."""
    print(f"Calling function: {context.function.name}")
    await next(context)
    print("Function call completed")

def get_time():
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

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
        middleware=[simple_function_middleware],
    )
    # Run the agent
    result = await agent.run("What time is it now in western, central and eastern  Australia (australia zone time and not in UTC) ?  SHow in a perfect aligned table using lines ")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
