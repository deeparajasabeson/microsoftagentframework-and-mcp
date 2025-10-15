// No need to start/run server project "MCP-API-MCPServer" while testing with MCP Server
// Just MCP-API-FackAPI server is enough to test CommerceTools.
// This program will run a command prompt process to start the MCP server project 
// Server hosts MCP tools that can be invoked by Tool Calling from Agent and LLM running by MCP Client(this project).
// CommerceTools are making http API calls to an external API server (MCP-API-FackAPI) to perform tool actions.

using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using ModelContextProtocol.Client;
using OpenAI;
using System.Diagnostics;
using System.Reflection;

static void AttachProcessExitHandler(StdioClientTransport transport)
{
    // If StdioClientTransport exposes internal underlying process, attach below:
    var process = GetUnderlyingProcess(transport);
    if (process != null)
    {
        process.EnableRaisingEvents = true;
        process.Exited += (s, e) =>
        {
            Console.WriteLine($"MCP Server process exited unexpectedly with code {process.ExitCode}");
            // Additional handling logic here
        };
    }
}

static Process? GetUnderlyingProcess(StdioClientTransport transport)
{
    if (transport == null) return null;

    var transportType = transport.GetType();

    // Try to find private field or property with Process type
    BindingFlags flags = BindingFlags.NonPublic | BindingFlags.Instance;

    // Search fields first
    foreach (var field in transportType.GetFields(flags))
    {
        if (field.FieldType == typeof(Process))
        {
            var process = field.GetValue(transport) as Process;
            if (process != null)
                return process;
        }
    }

    // If not found as field, search properties
    foreach (var prop in transportType.GetProperties(flags))
    {
        if (prop.PropertyType == typeof(Process) && prop.GetIndexParameters().Length == 0)
        {
            var process = prop.GetValue(transport) as Process;
            if (process != null)
                return process;
        }
    }
    // Not found
    return null;
}

// Step 0: API Tool setup
// -------------------------
Console.WriteLine("Defining MCP Tool wrapper...");
var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
const string modelName = "gpt-5-mini";
var instructions = "You are a helpful commerce agent.";
var agentName = "CommerceAgent";
StdioClientTransport? transport = null;

// 1. Setup stdio transport to spawn the server process
// -------------------------
Console.WriteLine("Spawning MCP Server Process...");
try { 
    transport = new StdioClientTransport(new StdioClientTransportOptions
    {
        Name = "LocalMcpServer",
        Command = "dotnet",
        Arguments = new[] { "run", "--project", "C:\\Deepa\\Learning\\AI-ML\\.Net Core\\Microsoft-Agent-Framework\\MCP-API-MCPServer\\MCP-API-MCPServer.csproj" }
    });
    // Optionally attach to underlying process exit event if accessible
    AttachProcessExitHandler(transport);

    // Await connection or any startup band check as per SDK
    await transport.ConnectAsync();

    Console.WriteLine("MCP Server process started successfully.");
    // proceed with MCP client workflows using transport...
}
catch (Exception ex)
{
    Console.WriteLine("--- MCP Server startup failure ---");
    Console.WriteLine($"Type: {ex.GetType().Name}");
    Console.WriteLine($"Message: {ex.Message}");
    Console.WriteLine($"Stack: {ex.StackTrace}");
}

// 2. Create an MCP stdio transport to the server
// -------------------------
try
{
    Console.WriteLine("Going to create MCP Client...");
    await using var mcpClient = await McpClient.CreateAsync(transport);
    Console.WriteLine("MCP Client created successfully.");
    Console.WriteLine("Continuing the process...");
    // 3. Discover tools from the MCP server
    // -------------------------
    Console.WriteLine("Discovering tools from MCP server...");
    var toolList = await mcpClient.ListToolsAsync();
    Console.WriteLine($"Discovered {toolList.ToList().Count} tools from MCP server:");
    foreach (var tool in toolList.ToList())
    {
        Console.WriteLine($" - {tool.Name}: {tool.Description}");
    }


    // 4. Configure  AI client 
    // -------------------------
    Console.WriteLine("=== AI Agent with MCP tools client ===");
    AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                                    .GetChatClient(modelName)
                                    .CreateAIAgent(
                                            instructions: instructions, 
                                            name: agentName,
                                            tools: toolList.ToArray());


    // 5. Interaction loop
    // -------------------------
    Console.WriteLine("\nYou may now ask questions (type ‘exit’ to quit).");
    while (true)
    {
        Console.Write("\nYou: ");
        string? user = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(user) || user.Equals("exit", StringComparison.OrdinalIgnoreCase))
            break;

        var agentResponse = await agent.RunAsync(user);
        Console.WriteLine("\nAgent: " + agentResponse.Text);
    }
}
catch (Exception ex)
{
    Console.WriteLine("Exception occurred :");
    Console.WriteLine($"Type: {ex.GetType().Name}");
    Console.WriteLine($"Message: {ex.Message}");
    Console.WriteLine($"StackTrace: {ex.StackTrace}");
    Console.WriteLine($"Full Exception: {ex}");
}
Console.WriteLine("Done.");
Console.ReadKey();