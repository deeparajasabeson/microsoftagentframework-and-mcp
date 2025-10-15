
import asyncio
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureOpenAIChatClient

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

# **Using an agent as a function tool**
# Can use a ChatAgent as a function tool by calling .as_tool() 
# on the agent and providing it as a tool to another agent. 
# This allows to compose agents and build more advanced workflows.
weather_agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    name="WeatherAgent",
    description="An agent that answers questions about the weather.",
    instructions="You answer questions about the weather.",
    tools=get_weather
)

#Convert weather_agent to a function tool::
main_agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    instructions="You are a helpful assistant who responds in Tamil.",
    tools=weather_agent.as_tool(
      name="WeatherLookup",
      description="Look up weather information for any location",
      arg_name="query",
      arg_description="The weather query or location"
    )
)

async def main():
    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
