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

async def main():
    async for update in agent.run_stream("Tell me a joke about a pirate."):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line after streaming is complete

if __name__ == "__main__":
    asyncio.run(main())