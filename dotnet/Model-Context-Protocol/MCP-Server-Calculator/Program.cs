using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(consoleLogOptions =>
{
    // Configure all logs to go to stderr
    consoleLogOptions.LogToStandardErrorThreshold = LogLevel.Trace;
});

builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class CalculatorTool
{
    [McpServerTool, Description("Adds two numbers")]
    public static string add(int a, int b) => $"Sum {a + b}";

    [McpServerTool, Description("Substract two numbers")]
    public static string subtract(int a, int b) => $"Subtract {a - b}";

    [McpServerTool, Description("Multiply two numbers")]
    public static string multiply(int a, int b) => $"Multiply {a * b}";

    [McpServerTool, Description("Divides two numbers")]
    public static string divide(int a, int b) => $"Divide {a / b}";
}
