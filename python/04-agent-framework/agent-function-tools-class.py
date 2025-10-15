import asyncio
from agent_framework import ai_function
from agent_framework.azure import AzureOpenAIChatClient

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

class WeatherTools:
    def __init__(self):
        self.last_location = None

    def get_weather(self, location:str) -> str:
        """Get the weather for a given location."""
        self.last_location = location
        return f"The weather in {location} is rainy with a high of 20°C."

    def get_weather_details(self) -> str:
        """Get the detailed weather for the last specified location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detailed weather in {self.last_location} is rainy with thunderstorm with a high of 23°C, low of 14°C, and 60% humidity."


tools = WeatherTools()

@ai_function(
    name="weather_tool",
    description="Retrieves weather information for any location"
)
def weather_tool(location: str) -> str:
    return tools.get_weather(location)

@ai_function(
    name="weather_details_tool",
    description="Retrieves detailed weather information for the last specified location"
)
def weather_details_tool() -> str:
    return tools.get_weather_details()

agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    instructions="You are a helpful assistant",
    tools=[weather_tool, weather_details_tool]
)

async def main():
    result = await agent.run("What is the weather like in Amsterdam ?")
    print(result.text)

    # 2. Ask for more details (no location specified)
    result = await agent.run("Can you give me detailed weather information for the last specified location ?")
    print(result.text)
    # -> Calls weather_details_tool(), which uses last_location ("Amsterdam")

if __name__ == "__main__":
    asyncio.run(main()) 