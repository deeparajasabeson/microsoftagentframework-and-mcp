// This is a simple ASP.NET Core application that should run always alongside the MCP server to provide mock API endpoints for testing.
// MCP server (MCP-API-MCPServer) will call these endpoints via CommerceTools.
// The endpoints simulate a product and order API with basic data.
// Through Agent/LLM in MCP client (MCP-API-MCPClient) you can invoke CommerceTools that will call these endpoints.
// Also through web api calls from "MCP-API-MCPClient-WebClient" you can call these endpoints via MCP server "MCP-API-MCPServer-HttpTransport".

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseExtraRoutes();

app.Run();
