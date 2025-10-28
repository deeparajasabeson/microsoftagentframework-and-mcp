using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;
using System.Text;
using System.Text.Json;

/**
 * Complete C# MCP Client Example
 * 
 * This client demonstrates how to:
 * 1. Connect to an GitHub MCP server
 * 2. List available tools and resources
 * 3. List all Repositories of a specific person
 */

Console.WriteLine("🚀 Creating MCP C# Client that connects to GitHub MCP Server...");

try
{
    // Create configuration builder
    var builder = Host.CreateApplicationBuilder(args);

    builder.Configuration
        .AddEnvironmentVariables()
        .AddUserSecrets<Program>();

    // Create stdio transport to connect to the MCP server
    Console.WriteLine("📡 Connecting to GitHub MCP server...");
    await using var mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new()
    {
        Name = "GitHub Server",
        Command = "npx",
        Arguments = ["-y", "@modelcontextprotocol/server-github"]
    }));
    Console.WriteLine("✅ Connected to MCP server successfully!");

    // List available tools
    Console.WriteLine("\n📋 Listing available tools:");
    var tools = await mcpClient.ListToolsAsync();
    foreach (var tool in tools)
    {
        Console.WriteLine($"  - {tool.Name}: {tool.Description}");
    }

    Console.WriteLine("\n📦 Fetching all repositories for a specific GitHub user...");
    string githubUsername = "deeparajasabeson";
    var result = await mcpClient.CallToolAsync(
        "search_repositories",
        new Dictionary<string, object?>()
        {
            ["query"] = $"user:{githubUsername}"
        },
        cancellationToken: CancellationToken.None
    );

    Console.WriteLine($"\n📁 Repositories of user '{githubUsername}':");
    foreach (TextContentBlock block in result.Content.OfType<TextContentBlock>())
    {
        Console.WriteLine($"Content : {block.Text}\n");
    }

    Console.WriteLine("\n✨ Client operations completed successfully!");
    Console.WriteLine("\nPress any key to continue...\n");
    Console.ReadKey();
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error running MCP client: {ex.Message}");
    Console.WriteLine($"Stack trace: {ex.StackTrace}");
    Console.WriteLine("\nPress any key to continue...\n");
    Console.ReadKey();
}