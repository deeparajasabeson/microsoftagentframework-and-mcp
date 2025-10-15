// This sample shows how to add a basic custom memory component to an agent.
// The memory component subscribes to all messages added to the conversation and
// extracts the user's name and age if provided.
// The component adds a prompt to ask for this information if it is not already known
// and provides it to the model before each invocation if known.

using System.Text;
using System.Text.Json;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using OpenAI;
using OpenAI.Chat;
using SampleApp;

var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
var modelName = "gpt-5-mini";

var instructions = "You are a friendly assistant. Always address the user by their name.";
var agentName = "Assistant";

ChatClient chatClient = new AzureOpenAIClient(endpoint, credential)
                                          .GetChatClient(modelName);


// Create the agent and provide a factory to add our custom memory component to
// all threads created by the agent. Here each new memory component will have its own
// user info object, so each thread will have its own memory.
// In real world applications/services, where the user info would be persisted in a database,
// and preferably shared between multiple threads used by the same user, ensure that the
// factory reads the user id from the current context and scopes the memory component
// and its storage to that user id.
AIAgent agent = chatClient.CreateAIAgent(new ChatClientAgentOptions()
{
    Name = agentName,
    Instructions = instructions,
    AIContextProviderFactory = ctx => new UserInfoMemory(
                                                chatClient.AsIChatClient(), 
                                                ctx.SerializedState, 
                                                ctx.JsonSerializerOptions)
});

// Create a new thread for the conversation.
AgentThread thread = agent.GetNewThread();
Console.WriteLine(">> Use thread with blank memory\n");

// Invoke the agent and output the text result.
Console.WriteLine(await agent.RunAsync("Hello, what is the square root of 9?", thread));
Console.WriteLine(await agent.RunAsync("My name is Ruaidhrí", thread));
Console.WriteLine(await agent.RunAsync("I am 20 years old", thread));

// We can serialize the thread. The serialized state will include the state of the memory component.
var threadElement = thread.Serialize();

Console.WriteLine("\n>> Use deserialized thread with previously created memories\n");

// Later we can deserialize the thread and continue the conversation with the previous memory component state.
var deserializedThread = agent.DeserializeThread(threadElement);
Console.WriteLine(await agent.RunAsync("What is my name and age?", deserializedThread));
Console.WriteLine("\n>> Read memories from memory component\n");

// It's possible to access the memory component via the thread's GetService method.
var userInfo = deserializedThread.GetService<UserInfoMemory>()?.UserInfo;

// Output the user info that was captured by the memory component.
Console.WriteLine($"MEMORY - User Name: {userInfo?.UserName}");
Console.WriteLine($"MEMORY - User Age: {userInfo?.UserAge}");
Console.WriteLine("\n>> Use new thread with previously created memories\n");

// It is also possible to set the memories in a memory component on an individual thread.
// This is useful if we want to start a new thread, but have it share the same memories as a previous thread.
var newThread = agent.GetNewThread();
if (userInfo is not null && newThread.GetService<UserInfoMemory>() is UserInfoMemory newThreadMemory)
{
    newThreadMemory.UserInfo = userInfo;
}

// Invoke the agent and output the text result.
// This time the agent should remember the user's name and use it in the response.
Console.WriteLine(await agent.RunAsync("What is my name and age?", newThread));
Console.ReadKey();

namespace SampleApp
{
    /// <summary>
    /// Sample memory component that can remember a user's name and age.
    /// </summary>
    internal sealed class UserInfoMemory : AIContextProvider
    {
        private readonly IChatClient _chatClient;
        public UserInfo UserInfo { get; set; }

        public UserInfoMemory(IChatClient chatClient, UserInfo? userInfo = null)
        {
            this._chatClient = chatClient;
            this.UserInfo = userInfo ?? new UserInfo();
        }

        public UserInfoMemory(IChatClient chatClient, 
                              JsonElement serializedState, 
                              JsonSerializerOptions? jsonSerializerOptions = null)
        {
            this._chatClient = chatClient;
            this.UserInfo = serializedState.ValueKind == JsonValueKind.Object ?
                serializedState.Deserialize<UserInfo>(jsonSerializerOptions)! :
                new UserInfo();
        }

        public override async ValueTask InvokedAsync(InvokedContext context, 
                                                     CancellationToken cancellationToken = default)
        {
            // Try and extract the user name and age from the message if we don't have it already and it's a user message.
            if ((this.UserInfo.UserName is null || this.UserInfo.UserAge is null) && context.RequestMessages.Any(x => x.Role == ChatRole.User))
            {
                var result = await this._chatClient.GetResponseAsync<UserInfo>(
                    context.RequestMessages,
                    new ChatOptions()
                    {
                        Instructions = "Extract the user's name and age from the message if present. If not present return nulls."
                    },
                    cancellationToken: cancellationToken);

                this.UserInfo.UserName ??= result.Result.UserName;
                this.UserInfo.UserAge ??= result.Result.UserAge;
            }
        }

        public override ValueTask<AIContext> InvokingAsync(InvokingContext context, 
                                                           CancellationToken cancellationToken = default)
        {
            StringBuilder instructions = new();

            // If we don't already know the user's name and age, add instructions to ask for them, otherwise just provide what we have to the context.
            instructions
                .AppendLine(
                    this.UserInfo.UserName is null ?
                        "Ask the user for their name and politely decline to answer any questions until they provide it." :
                        $"The user's name is {this.UserInfo.UserName}.")
                .AppendLine(
                    this.UserInfo.UserAge is null ?
                        "Ask the user for their age and politely decline to answer any questions until they provide it." :
                        $"The user's age is {this.UserInfo.UserAge}.");

            return new ValueTask<AIContext>(new AIContext
            {
                Instructions = instructions.ToString()
            });
        }

        public override JsonElement Serialize(JsonSerializerOptions? jsonSerializerOptions = null)
        {
            return JsonSerializer.SerializeToElement(this.UserInfo, jsonSerializerOptions);
        }
    }

    internal sealed class UserInfo
    {
        public string? UserName { get; set; }
        public int? UserAge { get; set; }
    }
}