using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using ModelContextProtocol.AspNetCore.Authentication;
using MCP_Server_with_Auth.Tools;
using System.Net.Http.Headers;
using System.Security.Claims;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        var serverUrl = "http://localhost:7071/";
        var inMemoryOAuthServerUrl = "http://localhost:5142";

        builder.Services.AddAuthentication(options =>
        {
            options.DefaultChallengeScheme = McpAuthenticationDefaults.AuthenticationScheme;
            options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
        })
        .AddJwtBearer(options =>
        {
            // Configure to validate tokens from our in-memory OAuth server
            options.Authority = inMemoryOAuthServerUrl;
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ValidAudience = serverUrl, // Validate that the audience matches the resource metadata as suggested in RFC 8707
                ValidIssuer = inMemoryOAuthServerUrl,
                NameClaimType = "name",
                RoleClaimType = "roles"
            };

            options.Events = new JwtBearerEvents
            {
                OnTokenValidated = context =>
                {
                    var name = context.Principal?.Identity?.Name ?? "unknown";
                    var email = context.Principal?.FindFirstValue("preferred_username") ?? "unknown";
                    Console.WriteLine($"Token validated for: {name} ({email})");
                    return Task.CompletedTask;
                },
                OnAuthenticationFailed = context =>
                {
                    Console.WriteLine($"Authentication failed: {context.Exception.Message}");
                    return Task.CompletedTask;
                },
                OnChallenge = context =>
                {
                    Console.WriteLine($"Challenging client to authenticate with Entra ID");
                    return Task.CompletedTask;
                }
            };
        })
        .AddMcp(options =>
        {
            options.ResourceMetadata = new()
            {
                Resource = new Uri(serverUrl),
                ResourceDocumentation = new Uri("https://docs.example.com/api/weather"),
                AuthorizationServers = { new Uri(inMemoryOAuthServerUrl) },
                ScopesSupported = ["mcp:tools"],
            };
        });

        builder.Services.AddAuthorization();

        builder.Services.AddHttpContextAccessor();
        builder.Services.AddMcpServer()
            .WithTools<WeatherTools>()
            .WithHttpTransport();

        // Configure HttpClientFactory for weather.gov API
        builder.Services.AddHttpClient("WeatherApi", client =>
        {
            client.BaseAddress = new Uri("https://api.weather.gov");
            client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("weather-tool", "1.0"));
        });

        var app = builder.Build();

        app.UseAuthentication();
        app.UseAuthorization();

        // Use the default MCP policy name that we've configured
        app.MapMcp().RequireAuthorization();

        //Console.WriteLine($"Starting MCP server with authorization at {serverUrl}");
        //Console.WriteLine($"Using in-memory OAuth server at {inMemoryOAuthServerUrl}");
        //Console.WriteLine($"Protected Resource Metadata URL: {serverUrl}.well-known/oauth-protected-resource");
        //Console.WriteLine("Press any key to continue to run the MCP Server...");
        //Console.ReadKey();
        //Console.WriteLine("Press Ctrl+C to stop the server");
        
        app.Run(serverUrl);
    }
}