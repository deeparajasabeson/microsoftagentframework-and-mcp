// Need to start/run this server as Startup Project while testing with
// MCP client web project "MCP-API-MCPClient-Web along with MCP-API-FackAPI server to test CommerceTools.
// This MCP Server hosts MCP tools that can be invoked by the web client ("MCP-API-MCPClient-Web").
// CommerceTools are making http API calls to an external API server to perform tool actions.
// Rather TemperatureTool are simple tools that do not make any external API calls.
// Both types of tools can be invoked by making API calls by the web client ("MCP-API-MCPClient-Web").

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient()
                .AddMcpServer()
                .WithHttpTransport()            // HTTP transport (used for web clients)
                .WithToolsFromAssembly();       // auto-register [McpServerTool] methods in current assembly        

var app = builder.Build();

app.MapMcp();

app.Run();
