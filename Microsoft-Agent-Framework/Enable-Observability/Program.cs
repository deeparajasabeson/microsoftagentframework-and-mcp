// This sample shows how to create and use a simple AI agent with Azure OpenAI as the backend that logs telemetry using OpenTelemetry.

using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using OpenAI;
using OpenTelemetry;
using OpenTelemetry.Trace;

// Create a TracerProvider that exports to the console
using var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("agent-telemetry-source")
    .AddConsoleExporter()
    .Build();

var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
var modelName = "gpt-5-mini";
var instructions = "You are good at telling jokes.";
var agentName = "Joker";

// Create the agent and enable OpenTelemetry instrumentation
AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                        .GetChatClient(modelName)
                        .CreateAIAgent(instructions: instructions, name: agentName)
                        .AsBuilder()
                        .UseOpenTelemetry(sourceName: "agent-telemetry-source")
                        .Build();

Console.WriteLine(await agent.RunAsync("Tell me a joke about a pirate."));
Console.ReadKey();

//Activity.TraceId:            b49a9d5ec1091ff4b2e5bd662402d71e
//Activity.SpanId:             dedd613f553f0f0c
//Activity.TraceFlags:         Recorded
//Activity.DisplayName:        invoke_agent Joker
//Activity.Kind:               Client
//Activity.StartTime:          2025 - 10 - 03T22: 13:48.2367705Z
//Activity.Duration:           00:00:03.8993027
//Activity.Tags:
//    gen_ai.operation.name: chat
//    gen_ai.request.model: gpt - 5 - mini
//    gen_ai.provider.name: openai
//    server.address: agent - azureopenaiclient.openai.azure.com
//    server.port: 443
//    gen_ai.agent.id: 3f7e83af295c4b76bdabdc88d5045673
//    gen_ai.agent.name: Joker
//    gen_ai.response.finish_reasons: ["stop"]
//    gen_ai.response.id: chatcmpl - CMiK2Och7KfwZ0BoAif9q0QQyj84W
//    gen_ai.response.model: gpt - 5 - mini - 2025 - 08 - 07
//    gen_ai.usage.input_tokens: 25
//    gen_ai.usage.output_tokens: 218
//Instrumentation scope(ActivitySource):
//    Name: agent - telemetry - source
//Resource associated with Activity:
//    telemetry.sdk.name: opentelemetry
//    telemetry.sdk.language: dotnet
//    telemetry.sdk.version: 1.13.0
//    service.name: unknown_service: Enable - Observability

//Why couldn't the pirate learn the alphabet? Because he kept getting lost at C.