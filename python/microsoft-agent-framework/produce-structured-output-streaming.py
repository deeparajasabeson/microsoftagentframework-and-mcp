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

# Streaming response handling. When streaming, to get the structured output, 
# we need to collect all the updates and then access the final response value:
async def main():
    # Get structured response from streaming agent using AgentRunResponse.from_agent_response_generator
    # This method collects all streaming updates and combines them into a single AgentRunResponse
    final_response = await AgentRunResponse.from_agent_response_generator(
        agent.run_stream("Please provide information about John Abraham Steele, who is a 25-year-old Director of Development Unit.",
                        response_format=PersonInfo),
        output_format_type=PersonInfo,
    )
    if final_response.value:
        person_info = final_response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")

if __name__ == "__main__":
    asyncio.run(main())