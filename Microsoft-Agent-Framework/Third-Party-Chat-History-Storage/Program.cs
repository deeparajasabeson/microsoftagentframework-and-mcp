// This sample shows how to create and use a simple AI agent with a conversation that can be persisted to disk.

using OpenAI;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.SemanticKernel.Connectors.InMemory;
using Third_Party_Chat_History_Storage;


var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
var modelName = "gpt-5-mini";
var instructions = "You are good at telling jokes.";
var agentName = "Joker";

AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                        .GetChatClient(modelName)
                        .CreateAIAgent(new ChatClientAgentOptions
                         {
                             Name = agentName,
                             Instructions = instructions,
                             ChatMessageStoreFactory = ctx =>
                             {
                                 // Create a new chat message store for this agent that stores the messages in a vector store.
                                 return new VectorChatMessageStore(
                                                new InMemoryVectorStore(),
                                                ctx.SerializedState,
                                                ctx.JsonSerializerOptions);
                             }
                         });

Console.WriteLine(await agent.RunAsync("Tell me a joke.", cancellationToken: CancellationToken.None));
Console.ReadKey();
