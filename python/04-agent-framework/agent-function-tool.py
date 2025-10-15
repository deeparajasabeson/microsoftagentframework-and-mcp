import asyncio
from typing import Annotated
from pydantic import Field
from agent_framework import ai_function
from agent_framework.azure import AzureOpenAIChatClient

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

@ai_function(
    name="weather_tool",
    description="Retrieves weather information for any location",
)
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    name="WeatherAgent",
    instructions="You are a helpful agent that can retrieve weather information.",
    tools=get_weather
)

async def main():
    result = await agent.run("What is the weather like in Madurai?", debug=True)
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main()) 