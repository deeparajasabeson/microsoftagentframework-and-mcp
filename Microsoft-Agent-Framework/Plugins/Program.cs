// This sample shows how to use plugins with an AI agent. Plugin classes can
// depend on other services that need to be injected. In this sample, the
// AgentPlugin class uses the WeatherProvider and CurrentTimeProvider classes
// to get weather and current time information. Both services are registered
// in the service collection and injected into the plugin.
// Plugin classes may have many methods, but only some are intended to be used
// as AI functions. The AsAITools method of the plugin class shows how to specify
// which methods should be exposed to the AI agent.
// The agent is created using Azure OpenAI as the backend model provider and
// the Microsoft.Agents.AI library for agent functionality.

using OpenAI;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.DependencyInjection;

var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
const string modelName = "gpt-5-mini";

const string AgentName = "Assistant";
const string AgentInstructions = "You are a helpful assistant that helps people find information.";

// Create a service collection to hold the agent plugin and its dependencies.
// The plugin depends on WeatherProvider and CurrentTimeProvider registered above.
ServiceCollection services = new();
services.AddSingleton<WeatherProvider>();
services.AddSingleton<CurrentTimeProvider>();
services.AddSingleton<AgentPlugin>();

IServiceProvider serviceProvider = services.BuildServiceProvider();

// Create the agent and enable OpenTelemetry instrumentation
AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                        .GetChatClient(modelName)
                        .CreateAIAgent(
                            instructions: AgentInstructions,
                            name: AgentName,
                            tools: serviceProvider.GetRequiredService<AgentPlugin>().AsAITools().ToList(),
                            services: serviceProvider
                        );

Console.WriteLine(await agent.RunAsync("Tell me current time and weather in Raleigh."));
Console.ReadKey();

/// The agent plugin that provides weather and current time information.
internal sealed class AgentPlugin(WeatherProvider weatherProvider)
{
    public string GetWeather(string location)
    {
        return weatherProvider.GetWeather(location);
    }

    /// Gets the current date and time for the specified location.
    public DateTimeOffset GetCurrentTime(IServiceProvider sp, string location)
    {
        // Resolve the CurrentTimeProvider from the service provider
        var currentTimeProvider = sp.GetRequiredService<CurrentTimeProvider>();

        return currentTimeProvider.GetCurrentTime(location);
    }

    /// Returns the functions provided by this plugin.
    public IEnumerable<AITool> AsAITools()
    {
        yield return AIFunctionFactory.Create(this.GetWeather);
        yield return AIFunctionFactory.Create(this.GetCurrentTime);
    }
}

/// The weather provider that returns weather information.
internal sealed class WeatherProvider
{
    /// Gets the weather information for the specified location.
    public string GetWeather(string location)
    {
        return $"The weather in {location} is cloudy with a high of 15°C.";
    }
}

/// Provides the current date and time.
internal sealed class CurrentTimeProvider
{
    /// Gets the current date and time.
    public DateTimeOffset GetCurrentTime(string location)
    {
        return DateTimeOffset.Now;
    }
}