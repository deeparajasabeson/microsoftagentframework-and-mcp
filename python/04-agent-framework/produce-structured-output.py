""" Not all agent types support structured output. The ChatAgent supports structured output 
when used with compatible chat clients. When creating or running the agent, we can provide 
a Pydantic model that defines the structure of the expected output. """

import asyncio
from urllib import response
from pydantic import BaseModel
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import AgentRunResponse

class PersonInfo(BaseModel):
    """Information about a person."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

agent = AzureOpenAIChatClient(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name
).create_agent(
    name="HelpfulAssistant",
    instructions="You are a helpful assistant that extracts person information from text."
)

async def main():
    response = await agent.run(
        "Please provide information about Deepa Steele, who is a 53-year-old Software Engineer.",
        response_format=PersonInfo
    )

    # The agent response will contain the structured output in the value property, 
    # which can be accessed directly as a Pydantic model instance:

    if response.value:
        person_info = response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
    else:
        print("No structured data found in response")

if __name__ == "__main__":
    asyncio.run(main())