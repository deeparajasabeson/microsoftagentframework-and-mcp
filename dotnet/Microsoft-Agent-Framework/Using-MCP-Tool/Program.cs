// Connect to an MCP server and use its tools within Agent.

using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;
using OpenAI;

//Popular MCP servers include:
//@modelcontextprotocol/server-github: Access GitHub repositories and data
//@modelcontextprotocol/server-filesystem: File system operations
//@modelcontextprotocol/server-sqlite: SQLite database access

// Step 1: Setting Up an MCP Client
//First, create an MCP client that connects to your desired MCP server:
//Popular MCP Servers
//Common MCP servers you can use with Python Agent Framework:

//Calculator: uvx mcp-server - calculator - Mathematical computations
//Filesystem: uvx mcp-server-filesystem - File system operations
//GitHub: npx @modelcontextprotocol/server-github - GitHub repository access
//SQLite: uvx mcp-server-sqlite - Database operations

try
{
    // Create an MCPClient for the GitHub server
    await using var mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new StdioClientTransportOptions()
    {
        //A friendly name for MCP server connection
        Name = "MCPServer",
        //The executable to run the MCP server (here using npx to run a Node.js package)
        Command = "npx",
        //Command-line arguments passed to the MCP server
        Arguments = ["-y", "--verbose", "@modelcontextprotocol/server-github"],
    }));

    // Step 2: Retrieve the list of tools available on the GitHub server
    var mcpTools = await mcpClient.ListToolsAsync().ConfigureAwait(false);
    Console.WriteLine($"Available tools in GitHub MCP Server : \n");
    foreach (var tool in mcpTools.ToList())
    {
        Console.WriteLine($"- {tool.Name}: {tool.Description}");
    }
    Console.WriteLine("\n=============================================================================================================\n");

    //// Execute a tool (this would normally be driven by LLM tool invocations).
    //var result = await mcpClient.CallToolAsync(
    //    "echo",
    //    new Dictionary<string, object?>() { ["message"] = "Hello MCP!" },
    //    cancellationToken: CancellationToken.None);

    //// echo always returns one and only one text content object
    //Console.WriteLine(result.Content.First(c => c.Type == "text").ToString());

    // Step 3: Create Agent
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
                                instructions: JokerInstructions,
                                tools: mcpTools.Cast<AITool>().ToList()
                             );


    // Step 4: Invoke the agent and output the text result
    //Console.WriteLine(await agent.RunAsync("Summarize the last four commits to the microsoft/semantic-kernel repository?"));
    //Console.WriteLine(await agent.RunAsync("Summarize details about microsoft/semantic-kernel repository"));
    Console.WriteLine(await agent.RunAsync("List all repositories name and date of creation in 2 columns of deeparajasabeson in a lined perfect table sorted by creation date"));
    Console.WriteLine("Press any key to exit...");
    Console.ReadKey();
}
catch (Exception ex)
{
    Console.WriteLine($"Error : {ex.Message}");
    return;
}


