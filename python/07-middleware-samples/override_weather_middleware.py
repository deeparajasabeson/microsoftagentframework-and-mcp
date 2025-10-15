import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from typing import Callable, Awaitable, AsyncIterable
from agent_framework import (
    AgentRunContext,
    AgentRunResponse,
    AgentRunResponseUpdate,
    ChatAgent,
    ChatMessage,
    Role,
    TextContent,
)

# --- Azure OpenAI Configuration ---
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# --- Sample weather tool ---
async def get_weather(city: str) -> str:
    """Mock function simulating fetching weather info."""
    return f"The weather in {city} is 10°C with rain and strong winds.\n"


# --- Non-streaming run ---
async def run_non_streaming():
    print("\n🌤️ Running in non-streaming mode:")

    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="WeatherAgent",
        instructions="You are a Funny and Polite Chat Agent.",
        tools=[get_weather],
        middleware=[override_weather_middleware]
    )

    result = await agent.run("What's the weather in Paris?")
    print("🤖 Final Response:", result)


# --- Streaming run ---
async def run_streaming():
    print("\n🌤️ Running in streaming mode:")
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="WeatherAgent",
        instructions="You are a Funny and Polite Chat Agent.",
        tools=[get_weather],
        middleware=[override_weather_middleware]
    )

    # Streaming output
    async for update in agent.run_stream("What's the weather in Paris?"):
        if update.contents:
            print(update.contents[0].text, end="", flush=True)
    print()  # newline at the end

# --- Middleware that overrides weather results ---
async def override_weather_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Middleware that overrides weather results for both streaming and non-streaming."""

    # Step 1: Execute the original agent logic
    await next(context)

    # Step 2: Override results if present
    if context.result is not None:
        custom_message_parts = [
            "🌦️ Weather Override: ",
            "Perfect weather everywhere today! ",
            "22°C with gentle breezes. ",
            "Great day for outdoor activities! 🌤️"
        ]

        if context.is_streaming:
            # --- Streaming override ---
            async def override_stream() -> AsyncIterable[AgentRunResponseUpdate]:
                for chunk in custom_message_parts:
                    yield AgentRunResponseUpdate(contents=[TextContent(text=chunk)])

            context.result = override_stream()

        else:
            # --- Non-streaming override ---
            custom_message = "".join(custom_message_parts)
            context.result = AgentRunResponse(
                messages=[ChatMessage(role=Role.ASSISTANT, text=custom_message)]
            )

# --- Main entrypoint ---
async def main():
    print("Inside main")
    await run_non_streaming()
    await run_streaming()


if __name__ == "__main__":
    asyncio.run(main())
