using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using OpenAI;

class Program
{
    static async Task Main()
    {
        var endpoint = new Uri("https://agent-azureopenaiclient.openai.azure.com/");
        var credential = new Azure.AzureKeyCredential("Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg");
        var modelName = "gpt-5-mini";
        var instructions = "You are good at telling jokes.";
        var agentName = "Joker";

        try
        {
            AIAgent agent = new AzureOpenAIClient(endpoint, credential)
                .GetChatClient(modelName)
                .CreateAIAgent(instructions: instructions, name: agentName);

            var response = await agent.RunAsync("Tell me a very funny joke about a Baker.");
            Console.WriteLine(response);
            Console.ReadKey();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[UNEXPECTED ERROR] {ex.GetType().Name}: {ex.Message}");
            Console.WriteLine(ex.StackTrace);
        }
    }
}