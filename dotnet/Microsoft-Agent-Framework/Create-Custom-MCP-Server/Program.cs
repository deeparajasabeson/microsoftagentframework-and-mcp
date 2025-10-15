// Here is an example of how to create an MCP server and register all tools from the current application.

using Microsoft.Extensions.AI;
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

// Employed overload of WithTools examines the current assembly for classes with the McpServerToolType attribute, and
// registers all methods with the McpServerTool attribute as tools.
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class TestMCPServerTool
{
    [McpServerTool(Name = "EchoMessage"), Description("Echoes the message back to the client.")]
    public static string Echo(string message) => $"hello {message}";

    [McpServerTool(Name = "DelayEchoMessage"), Description("Echoes the message back to the client with Delay.")]
    public static async Task<string> EchoWithDelayAsync(string message, int delayInSeconds)
    {
        await Task.Delay(delayInSeconds * 1000);
        return $"hello {message} after {delayInSeconds} seconds delay";
    }

    [McpServerTool(Name = "Add2Numbers"), Description("Add given two number.")]
    public static int Add(int a, int b) => a + b;

    [McpServerTool(Name = "CurrentDateTime"), Description("Get current date and time.")]
    public static string GetDateTime() => DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

    [McpServerTool(Name = "GetAJoke"), Description("Get a random joke.")]
    public static string GetJoke()
    {
        var jokes = new[]
        {
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call fake spaghetti? An impasta!",
            "Why did the bicycle fall over? Because it was two-tired!"
        };
        var random = new Random();
        int index = random.Next(jokes.Length);
        return jokes[index];
    }

    [McpServerTool(Name ="EncryptMessage"), Description("Reverse a String.")]
    public static string Reverse(string message)
    {
        if (string.IsNullOrEmpty(message))
            return message;
        char[] charArray = message.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }

    [McpServerTool(Name = "SummarizeContentFromUrl"), Description("Summarizes content downloaded from a specific URI")]
    public static async Task<string> SummarizeDownloadedContent(
                                            McpServer thisServer,
                                            HttpClient httpClient,
                                            [Description("The url from which to download the content to summarize")] string url,
                                            CancellationToken cancellationToken)
    {
        string content = await httpClient.GetStringAsync(url);

        ChatMessage[] messages =
        [
            new(ChatRole.User, "Briefly summarize the following downloaded content:"),
            new(ChatRole.User, content),
        ];

        ChatOptions options = new()
        {
            MaxOutputTokens = 256,
            Temperature = 0.3f,
        };

        return $"Summary: {await thisServer.AsSamplingChatClient().GetResponseAsync(messages, options, cancellationToken)}";
    }

    [McpServerPromptType]
    public static class MyPrompts
    {
        [McpServerPrompt, Description("Creates a prompt to summarize the provided message.")]
        public static ChatMessage Summarize([Description("The content to summarize")] string content) =>
            new(ChatRole.User, $"Please summarize this content into a single sentence: {content}");
    }
}