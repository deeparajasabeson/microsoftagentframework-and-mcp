// This sample demonstrates how to expose an existing AI agent as an MCP tool.
// The agent is created using Azure OpenAI as the backend model provider and the Microsoft.Agents.AI library for agent functionality.
// The MCP server is created using the ModelContextProtocol.Server library and the agent is converted to an MCP tool using the McpServerTool class.
// To run the sample, please use one of the following MCP client Project in the same solution:--> MCP-Client-ConsoleApp

using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Server;
using OpenAI;
using Microsoft.Extensions.DependencyInjection;


var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
var modelName = "gpt-5-mini";
const string agentName = "Joker";
const string JokerDescription = "An agent that tells jokes.";
const string JokerInstructions = "You are good at telling jokes, and you always start each joke with 'Aye aye, captain!'.";

AIAgent agent = new AzureOpenAIClient(endpoint, credential)
    .GetChatClient(modelName)
    .CreateAIAgent(
        name: agentName,
        description: JokerDescription,
        instructions: JokerInstructions
     );

// Convert the agent to an AIFunction and then to an MCP tool.
// The agent name and description will be used as the mcp tool name and description.
McpServerTool tool = McpServerTool.Create(agent.AsAIFunction());

// Register the MCP server with StdIO transport and expose the tool via the server.
HostApplicationBuilder builder = Host.CreateEmptyApplicationBuilder(settings: null);
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport() // stdio for communication
    .WithTools([tool]);

await builder.Build().RunAsync();