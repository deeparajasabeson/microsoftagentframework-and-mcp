import asyncio
from agent_framework import ai_function
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import BaseAgent, AgentRunResponseUpdate

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

# STEP 1: Define the weather tool with internal state
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


# STEP 2: Instantiate the tool
tools = WeatherTools()


# STEP 3: Define tool functions with ai_function decorator
@ai_function(
    name="get_weather",
    description="Get the weather for a given location."
)
def get_weather(location: str) -> str:
    return weather_tool.get_weather(location)

@ai_function(
    name="get_weather_details",
    description="Get detailed weather for the last requested location."
)
def get_weather_details() -> str:
    return weather_tool.get_weather_details()



# STEP 4: Human-in-the-loop wrapper
# Wrapper tracks last location outside agent
class HumanInLoopAgent:
    def __init__(self, inner_agent: BaseAgent):
        self.inner_agent = inner_agent
        self.last_location = None  # Track last location here

    async def run(self, prompt: str) -> AgentRunResponseUpdate:
      print(f"\nHumanInLoopAgent received prompt: {prompt}")

      # Simple location extraction (could be improved)
      if "weather in " in prompt.lower():
          loc_start = prompt.lower().find("weather in ") + len("weather in ")
          location = prompt[loc_start:].strip().rstrip("?")
          if location:
              self.last_location = location
              print(f"Stored last_location: {self.last_location}")

      approval = input("Approve this request? (y/n): ").strip().lower()
      if approval != "y":
          print("Human rejected the prompt. No action taken.\n")
          return AgentRunResponseUpdate(text="Human said no. Aborting.")

      # If prompt asks for detailed weather for last location but doesn't specify it explicitly,
      # rewrite prompt to include the stored location.
      if ("detailed weather" in prompt.lower() or "weather details" in prompt.lower()) and \
        ("last specified location" in prompt.lower() or "last requested location" in prompt.lower()):
          if self.last_location:
              prompt = f"Can you give me detailed weather for {self.last_location}?"
              print(f"Modified prompt to include last location: {prompt}")
          else:
              return AgentRunResponse(text="No last location stored. Please specify a location.")

      print("Human approved the prompt. Calling inner agent...\n")
      return await self.inner_agent.run(prompt)



# STEP 5: Create the Azure OpenAI Agent
inner_agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    instructions="You are a helpful assistant.",
    tools=[get_weather, get_weather_details]
)

# Instantiate the human-in-the-loop wrapper agent
agent = HumanInLoopAgent(inner_agent=inner_agent)

async def main():
    for prompt in [
        "What's the weather in Amsterdam?",
        "Can you give me weather details for last specified location ?"
    ]:
        response = await agent.run(prompt)
        print(f"\nPrompt: {prompt}")
        if response.text:
            print(f"Agent: {response.text}")
        else:
            print("Agent returned empty response text.")

if __name__ == "__main__":
    asyncio.run(main())
