import asyncio
from agent_framework.azure import AzureOpenAIChatClient

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

agent = AzureOpenAIChatClient(
    # credential=AzureCliCredential(), # Use API key instead
    api_key=api_key, # Replace with your actual API key
    endpoint=endpoint, # Replace with your actual Azure OpenAI endpoint
    deployment_name=deployment_name # Replace with your actual deployment name
).create_agent(
    instructions="You are good at telling jokes.",
    name="Joker"
)

thread = agent.get_new_thread()

async def main():
    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
    print(result1.text)

    result2 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread)
    print(result2.text)

if __name__ == "__main__":
    asyncio.run(main())