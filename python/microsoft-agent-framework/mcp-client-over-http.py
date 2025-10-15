# MCPStreamableHTTPTool - HTTP/SSE MCP Servers
# Use MCPStreamableHTTPTool to connect to MCP servers over HTTP with Server-Sent Events:

import asyncio
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

async def http_mcp_example():
    """Example using an HTTP-based MCP server."""
    async with AzureCliCredential() as credential:
        # Get token for the Microsoft Docs MCP API
        token = await credential.get_token("https://learn.microsoft.com/.default")

    # Initialize the chat client using AzureOpenAIChatClient
    chat_client = AzureOpenAIChatClient(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )

    async with (
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            headers={"Authorization": f"Bearer {token.token}"}
        ) as mcp_server,
        ChatAgent(
            chat_client=chat_client,
            name="DocsAgent",
            instructions="You help with Microsoft documentation questions.",
        ) as agent,
    ):
        result = await agent.run(
            "How to create an Azure storage account using az cli?",
            tools=mcp_server
        )
        print ("Response from MCP server:")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(http_mcp_example())