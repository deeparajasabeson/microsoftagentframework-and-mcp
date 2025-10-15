// This sample Create a new OAuth Server - ready-to-run OAuth 2.0 server that can use to authenticate MCP Client.
// This will be a minimal server that issues JWT access tokens.

///..TESTING once server is running ..::
// curl -X POST http://localhost:5142/token
////{ 
///   "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJqdGkiOiJkYzNjOTU3MS0yMjQ1LTRjOTktODQ2YS1jYmM2ODFkMDY2ZjAiLCJleHAiOjE3NTk3NTM4OTYsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImF1ZCI6InRlc3QtYXVkaWVuY2UifQ.gpBTLKfOqqwGZ67vhtbw0notFwoG136O6MPlNB6C1HE",
///   "token_type": "Bearer",
///   "expires_in":3600
///}
//curl -H "Authorization: Bearer <JWT>" http://localhost:5142/protected  -- Replace <JWT> with access-token received in previous curl
//Hello from protected endpoint !

using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

var key = "super-secret-key-1234567890123456";// Change for your tests
var issuer = "http://localhost:5000";
var audience = "test-audience";

// Configure JWT authentication (optional if validating tokens internally)
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = issuer,
            ValidAudience = audience,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key))
        };
    });

builder.Services.AddAuthorization();
var app = builder.Build();

// Token endpoint
app.MapPost("/token", () =>
{
    var claims = new[]
    {
        new Claim(JwtRegisteredClaimNames.Sub, "test-user"),
        new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
    };

    var token = new JwtSecurityToken(
        issuer: issuer,
        audience: audience,
        claims: claims,
        expires: DateTime.UtcNow.AddHours(2),
        signingCredentials: new SigningCredentials(
            new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key)),
            SecurityAlgorithms.HmacSha256)
    );

    var jwt = new JwtSecurityTokenHandler().WriteToken(token);
    return Results.Json(new { access_token = jwt, token_type = "Bearer", expires_in = 3600*2 });
});

// Optional: protected test endpoint
app.MapGet("/protected", () => "Hello from protected endpoint!")
   .RequireAuthorization();

app.UseAuthentication();
app.UseAuthorization();

app.Run();
