import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import HostedMCPTool

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

async def main():
    print("Creating agent...")
    agent = AzureOpenAIChatClient(
        api_key=api_key, 
        endpoint=endpoint, 
        deployment_name=deployment_name 
    ).create_agent(
        name="MicrosoftLearnAgent", 
        instructions="You answer questions by searching Microsoft Learn content only.",
        tools=HostedMCPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        ))
    print("Running agent...")
    result = await agent.run("What is Azure OpenAI?")
    print(result.text)
    
if __name__ == "__main__":
     asyncio.run(main())