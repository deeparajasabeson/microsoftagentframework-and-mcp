//// This sample shows how to create and use a simple AI agent with a conversation that can be persisted to disk.
//// It uses Azure OpenAI as the backend model provider and the Microsoft.Agents.AI library for agent functionality.
//// The conversation thread is serialized to JSON and saved to a local file, then reloaded and resumed later.
//// Make sure to replace the endpoint and key with your own Azure OpenAI service details.
//// // Note: In production, consider using secure storage for the serialized conversation instead of a local file.

using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using OpenAI;
using System.Text.Json;

var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
var modelName = "gpt-5-mini";
var instructions = "You are a helpful assistant.";
var agentName = "Assistant";

// Create the agent and enable OpenTelemetry instrumentation
AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                        .GetChatClient(modelName)
                        .CreateAIAgent(instructions: instructions, name: agentName);

AgentThread thread = agent.GetNewThread();
// Run the agent and append the exchange to the thread
Console.WriteLine(await agent.RunAsync("Tell me a short pirate joke.", thread));

// Serialize the thread state
JsonElement serializedThread = thread.Serialize();
string serializedJson = JsonSerializer.Serialize(serializedThread, JsonSerializerOptions.Web);

// Example: save to a local file (replace with DB or blob storage in production)
string filePath = Path.Combine(Path.GetTempPath(), "agent_thread.json");
await File.WriteAllTextAsync(filePath, serializedJson);

// Read persisted JSON
string loadedJson = await File.ReadAllTextAsync(filePath);
JsonElement reloaded = JsonSerializer.Deserialize<JsonElement>(loadedJson);

// Deserialize the thread into an AgentThread tied to the same agent type
AgentThread resumedThread = agent.DeserializeThread(reloaded);

// Continue the conversation with resumed thread
Console.WriteLine(await agent.RunAsync("Now tell that same joke in the voice of a pirate with some funny emojis all over the joke text.", resumedThread));
Console.ReadKey();
