# ***************************
#  NOT WORKING - NEEDS FIXING
# ***************************
import asyncio
from agent_framework import ChatAgent, MCPWebsocketTool
from agent_framework.openai import OpenAIChatClient
from agent_framework.azure import AzureOpenAIChatClient

api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"

async def websocket_mcp_example():
    # Initialize the chat client using AzureOpenAIChatClient
    chat_client = AzureOpenAIChatClient(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )

    """Example using a WebSocket-based MCP server."""
    async with (
        MCPWebsocketTool(
            name="realtime-data",
            url="wss://api.example.com/mcp",
        ) as mcp_server,
        ChatAgent(
            chat_client=chat_client,
            name="DataAgent",
            instructions="You provide real-time data insights.",
        ) as agent,
    ):
        result = await agent.run(
            "What is the current market status?",
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(websocket_mcp_example())
