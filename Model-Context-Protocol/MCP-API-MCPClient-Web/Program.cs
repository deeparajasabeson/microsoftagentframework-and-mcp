using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
McpClientOptions mcpClientOptions = new()
{
    ClientInfo = new() { Name = "MCP-API-MCPClient-Web", Version = "1.0.0" }
};

SseClientTransport sseClientTransport = new( new() 
{ 
    Endpoint = new Uri("https://localhost:7121"), 
    Name = "SseTransport"
});

// Register MCP Client services for dependency injection
builder.Services.AddTransient<Task<IMcpClient>>((sp) => { 
    return McpClientFactory.CreateAsync(sseClientTransport, mcpClientOptions); 
});

var app = builder.Build();


// Configure the HTTP request pipeline.

app.UseHttpsRedirection();
app.MapGet("/get_product_details", async Task<IResult> (Task<IMcpClient> mcpClientTask, decimal id) => { 
    Dictionary<string, object?> arguments = new() {
        ["productId"] = id
    };
    var mcpClient = await mcpClientTask;

    // List all available tools
    var tools = await mcpClient.ListToolsAsync();

    foreach(var tool in tools)
    {
        Console.WriteLine($" - {tool.Name} : {tool.Description}");
    }

    var response = await mcpClient.CallToolAsync("get_product_details", arguments).ConfigureAwait(false);

    if(!response.IsError && response.Content != null) {
        if(response.Content.Count > 0)
        {
            ContentBlock contentBlock = response.Content[0];
            var text = ((TextContentBlock)contentBlock).Text;

            return TypedResults.Ok(text);
        }
    }

    return TypedResults.BadRequest();
});

app.MapGet("/ConvertF2C", async Task<IResult> (Task<IMcpClient> mcpClientTask, decimal temp) => {
    Dictionary<string, object?> arguments = new()
    {
        ["fTemp"] = temp
    };
    var mcpClient = await mcpClientTask;

    // List all available tools
    var tools = await mcpClient.ListToolsAsync();

    foreach (var tool in tools)
    {
        Console.WriteLine($" - {tool.Name} : {tool.Description}");
    }

    var response = await mcpClient.CallToolAsync("ConvertF2C", arguments).ConfigureAwait(false);

    if (!response.IsError && response.Content != null)
    {
        if (response.Content.Count > 0)
        {
            ContentBlock contentBlock = response.Content[0];
            var text = ((TextContentBlock)contentBlock).Text;

            return TypedResults.Ok(text);
        }
    }

    return TypedResults.BadRequest();
});

app.Run();
