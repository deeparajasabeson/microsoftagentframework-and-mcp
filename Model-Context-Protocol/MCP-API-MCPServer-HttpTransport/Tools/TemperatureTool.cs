// Temperature conversion tool for MCP Server  with HTTP transport
// Simple example tool that does not require HttpClientFactory or not making any external API (Http) Calls.

using ModelContextProtocol.Server;
using System.ComponentModel;

namespace MCP_API_MCPServer_HttpTransport.Tools
{
    [McpServerToolType]
    public class TemperatureTool
    {
        [McpServerTool, Description("Convert Fahrenheit to Celsius")]
        public static double ConvertF2C([Description("Fahrenheit temperature to convert")] double fTemp)
        {
            return (fTemp - 32) * 5.0 / 9.0;
        }
    }
}
