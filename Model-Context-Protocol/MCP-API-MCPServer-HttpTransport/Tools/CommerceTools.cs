// All Tools in CommerceTools are making http API calls to an external
// running API server (MCP-API-FackAPI project) to perform tool actions.

using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;
using System.ComponentModel;
using System.Text.Json;

[McpServerToolType] // allows automatic discovery
public class CommerceTools
{
    private readonly IHttpClientFactory _httpClientFactory;

    public CommerceTools(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    [McpServerTool(Name = "get_product_details")]
    [Description("Fetches product details from the external Product API.")]
    public async ValueTask<CallToolResult> GetProductDetailsAsync(
        [Description("Product ID to fetch")] int productId)
    {
        return await CallExternalApiAsync("product", productId);
    }

    [McpServerTool(Name = "get_order_details")]
    [Description("Fetches order details from the external Order API.")]
    public async ValueTask<CallToolResult> GetOrderDetailsAsync(
        [Description("Order ID to fetch")] int orderId)
    {
        return await CallExternalApiAsync("order", orderId);
    }

    // Shared helper for both tools
    private async ValueTask<CallToolResult> CallExternalApiAsync(string type, int id)
    {
        var baseUrl = "https://localhost:7144";
        var http = _httpClientFactory.CreateClient("commerce");
        var url = $"{baseUrl.TrimEnd('/')}/{type}s/{id}";

        try
        {
            using var response = await http.GetAsync(url);
            var statusCode = (int)response.StatusCode;
            var responseHeaders = response.Headers.ToString();
            var responseBody = await response.Content.ReadAsStringAsync();
            if (!response.IsSuccessStatusCode)
            {
                // Return detailed error report on HTTP error status codes
                return BuildErrorReport(
                    $"HTTP {(int)response.StatusCode} {response.ReasonPhrase}",
                    "GET",
                    url,
                    null,
                    statusCode,
                    responseHeaders,
                    responseBody,
                    null);
            }

            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            using var doc = JsonDocument.Parse(json);

            // Simplify to human-readable summary
            var result = doc.RootElement.GetRawText();

            return new CallToolResult
            {
                Content = new[]
                {
                    new TextContentBlock
                    {
                        Type = "text",
                        Text = $"✅ {type.ToUpper()} details for ID {id}:\n\n{result}"
                    }
                }
            };
        }
        catch (HttpRequestException ex)
        {
            return Error($"HTTP error: {ex.Message}");
        }
        catch (Exception ex)
        {
            return Error($"Unexpected error: {ex.Message}");
        }
    }

    private CallToolResult Error(string message) =>
        new()
        {
            Content = new[]
            {
                new TextContentBlock { Type = "text", Text = "❌ " + message }
            }
        };

    private CallToolResult BuildErrorReport(
                                string errorType,
                                string httpMethod,
                                string url,
                                string? requestBody,
                                int? statusCode,
                                string? responseHeaders,
                                string? responseBody,
                                Exception? exception)
    {
        var exceptionType = exception?.GetType().FullName ?? "N/A";
        var exceptionMessage = exception?.Message ?? errorType;
        var stackTrace = exception?.StackTrace ?? "N/A";

        string errorReport = $@"
        - Request:
          - HTTP method: {httpMethod}
          - URL: {url}
          - Body: {(requestBody ?? "N/A")}
        - Response:
          - HTTP status code: {(statusCode?.ToString() ?? "N/A")}
          - Response headers: {(responseHeaders ?? "N/A")}
          - Response body: {(responseBody ?? "N/A")}
        - Server-side exception:
          - Exception type: {exceptionType}
          - Message: {exceptionMessage}
          - Stack trace: {IndentLines(stackTrace, 4)}";

        return new CallToolResult
        {
            Content = new[]
            {
                new TextContentBlock
                {
                    Type = "text",
                    Text = "❌ Error occurred:\n" + errorReport.Trim()
                }
            }
        };
    }

    private string IndentLines(string text, int indentSpaces)
    {
        var indent = new string(' ', indentSpaces);
        var lines = text.Split(new[] { "\r\n", "\r", "\n" }, StringSplitOptions.None);
        return string.Join("\n", lines.Select(line => indent + line));
    }
}
