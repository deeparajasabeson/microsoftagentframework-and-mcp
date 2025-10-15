# Using MCP tools with Agents
# The Microsoft Agent Framework supports integration with Model Context Protocol (MCP) servers, 
# allowing agents to access and use external tools and services within agent.
# Use MCPStdioTool to connect to MCP servers that run as local processes using standard input/output:

import asyncio
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async def main():
    """Example using a local MCP server via stdio."""
    async with (
        MCPStdioTool(
            name="calculator", 
            command="uvx", 
            args=["mcp-server-calculator"]
        ) as mcp_server,
        ChatAgent(
            chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
            name="MathAgent",
            instructions="You are a helpful math assistant that can solve calculations.",
        ) as agent,
    ):
        result = await agent.run(
            "What is 1500 * 23 + 45?", 
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())

