// No need to start/run this server while testing with MCP client project "MCP-API-MCPClient"
// Just MCP-API-FackAPI server is enough to test CommerceTools.
// This server will be run by the MCP client and communicates via stdio.
// It hosts MCP tools that can be invoked by the client.
// CommerceTools are making http API calls to an external API server to perform tool actions.

var builder = Host.CreateApplicationBuilder(args);

// send all console logs to stderr (useful for MCP stdio transport)
builder.Logging.AddConsole(options =>
{
    options.LogToStandardErrorThreshold = LogLevel.Trace;
});

builder.Services
    .AddHttpClient()
    .AddMcpServer()
    .WithStdioServerTransport()      // stdio transport (used by VS Code / clients)
    .WithToolsFromAssembly();       // auto-register [McpServerTool] methods in current assembly

var app = builder.Build();

await app.RunAsync();
