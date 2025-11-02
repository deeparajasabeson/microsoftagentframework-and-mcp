using System.ComponentModel;
using ModelContextProtocol.Server;

namespace MCP_Server_HttpSteaming_Calculator
{
    [McpServerToolType]
    public sealed class Tools
    {
        [McpServerTool, Description("Add two numbers together.")]
        public async Task<string> AddNumbers(
            [Description("The first number")] int a,
            [Description("The second number")] int b)
        {
            return await Task.FromResult((a + b).ToString());
        }

        [McpServerTool, Description("Subtract number from first number.")]
        public async Task<string> SubtractNumbers(
            [Description("The first number")] int a,
            [Description("The second number")] int b)
        {
            return await Task.FromResult((a - b).ToString());
        }

        [McpServerTool, Description("Multiply two numbers together.")]
        public async Task<string> MultiplyNumbers(
            [Description("The first number")] int a,
            [Description("The second number")] int b)
        {
            return await Task.FromResult((a * b).ToString());
        }

        [McpServerTool, Description("Divide first number by second number.")]
        public async Task<string> DivideNumbers(
            [Description("The first number")] int a,
            [Description("The second number")] int b)
        {
            return await Task.FromResult((a / b).ToString());
        }

        [McpServerTool, Description("Power to first number.")]
        public async Task<string> PowerNumbers(
            [Description("The first number")] double a,
            [Description("The second number")] double b)
        {
            return await Task.FromResult(Math.Pow(a, b).ToString());
        }

    }
}
