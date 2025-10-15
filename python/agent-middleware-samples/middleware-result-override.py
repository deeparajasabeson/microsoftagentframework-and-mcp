import asyncio
from typing import AsyncIterable
from agent_framework import ChatMessage, AgentRunResponse, Role, AgentRunResponseUpdate
from agent_framework import ChatAgent, agent_middleware, AgentRunContext
from typing import Callable, Awaitable
from agent_framework.azure import AzureOpenAIChatClient

async def weather_override_middleware(
    context: AgentRunContext, 
    next: Callable[[AgentRunContext], Awaitable[None]]
) -> None:
    """Middleware that overrides weather results for both streaming and non-streaming."""

    # Execute the original agent logic
    await next(context)

    # Override results if present
    if context.result is not None:
        custom_message_parts = [
            "Weather Override: ",
            "Perfect weather everywhere today! ",
            "22°C with gentle breezes. ",
            "Great day for outdoor activities!"
        ]

        if context.is_streaming:
            # Streaming override
            async def override_stream() -> AsyncIterable[AgentRunResponseUpdate]:
                for chunk in custom_message_parts:
                    yield AgentRunResponseUpdate(contents=[TextContent(text=chunk)])

            context.result = override_stream()
        else:
            # Non-streaming override
            custom_message = "".join(custom_message_parts)
            context.result = AgentRunResponse(
                messages=[ChatMessage(role=Role.ASSISTANT, text=custom_message)]
            )
    else :
        print("No result to override")

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

agent = ChatAgent(
    chat_client=AzureOpenAIChatClient(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    ),
    name="GreetingAgent",
    instructions="You are a friendly greeting assistant.",
    middleware=[weather_override_middleware],
)

async def main():
    # Run the agent
    result = await agent.run("blocked content")
    print(result.text)

    # result = await agent.run("Hello !")
    # print(result.text)

if __name__ == "__main__":
     asyncio.run(main())