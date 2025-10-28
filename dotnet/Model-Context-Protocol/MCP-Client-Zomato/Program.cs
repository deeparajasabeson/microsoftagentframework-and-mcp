using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;
using System.Text.Json;

/**
 * Complete C# MCP Client Example
 * 
 * This client demonstrates how to:
 * 1. Connect to an GitHub MCP server
 * 2. List available tools and resources
 * 3. List all Repositories of a specific person
 */

Console.WriteLine("🚀 Creating MCP C# Client that connects to Zomato MCP Server...");

try
{
    // Create configuration builder
    var builder = Host.CreateApplicationBuilder(args);

    builder.Configuration
        .AddEnvironmentVariables()
        .AddUserSecrets<Program>();

    // Create stdio transport to connect to the MCP server
    Console.WriteLine("📡 Connecting to Zomato MCP server...");
    await using var mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new()
    {
        Name = "GitHub Server",
        Command = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\mcp-remote.cmd",
        Arguments = ["https://mcp-server.zomato.com/mcp"]
    }));
    Console.WriteLine("✅ Connected to Zomato MCP server successfully!");

    // List available tools
    Console.WriteLine("\n📋 Listing available tools in Zomato MCP Server :");
    var tools = await mcpClient.ListToolsAsync();
    var indexer = 0;
    foreach (var tool in tools)
    {
        Console.WriteLine($"{++indexer} - {tool.Name}: {tool.Description} - {tool.JsonSchema}");
        Console.WriteLine("\n===========================================================================================================================\n");
    }
    
    Console.WriteLine("\n📦 Fetching all restaurants near user location...");
    var result = await mcpClient.CallToolAsync(
        "get_saved_addresses_for_user",
    new Dictionary<string, object?>()
    {
    },
        cancellationToken: CancellationToken.None
    );

    Console.WriteLine($"\n📁 Saved addresses for user :");
    foreach (TextContentBlock block in result.Content.OfType<TextContentBlock>())
    {
        var addressesResult = JsonSerializer.Deserialize<AddressesResult>(block.Text);
        if (addressesResult?.addresses?.Count > 0)
        {
            Console.WriteLine("\n🍽 Registered addresses :\n");
            foreach (var address in addressesResult.addresses)
            {
                Console.WriteLine($"Latitude: {address.latitude}");
                Console.WriteLine($"Longitude: {address.longitude}");
                Console.WriteLine($"Short Name: {address.short_name}");
                Console.WriteLine($"Full Name: {address.full_name}");
                Console.WriteLine($"Cell ID: {address.cell_id}");
                Console.WriteLine($"Delivery Subzone ID: {address.delivery_subzone_id}");
                Console.WriteLine($"Place ID: {address.place_id}");
                Console.WriteLine($"Place Type: {address.place_type}");
                Console.WriteLine($"Address ID: {address.address_id}");
                Console.WriteLine($"Cell Details:");

                if(address.cell_details != null){
                    Console.WriteLine($"    Country ID - {address.cell_details.country_id}");
                    Console.WriteLine($"    City ID - {address.cell_details.city_id}");
                    Console.WriteLine($"    DSZ ID - {address.cell_details.dsz_id}");
                    Console.WriteLine($"    Cell ID - {address.cell_details.cell_id}");
                }
                Console.WriteLine(new string('-', 40));
            }
        }
    }

    var addressesJson = result.Content.OfType<TextContentBlock>().LastOrDefault()?.Text;
    var addressesDict = JsonSerializer.Deserialize<Dictionary<string, object>>(addressesJson);
    var locationAddress = ((JsonElement)addressesDict["addresses"])[0]; // second address
    var userLocation = new Dictionary<string, object?>
    {
        ["latitude"] = locationAddress.GetProperty("latitude").GetString(),
        ["longitude"] = locationAddress.GetProperty("longitude").GetString(),
        ["short_name"] = locationAddress.GetProperty("short_name").GetString(),
        ["full_name"] = locationAddress.GetProperty("full_name").GetString(),
        ["cell_id"] = locationAddress.GetProperty("cell_id").GetString(),
        ["delivery_subzone_id"] = locationAddress.GetProperty("delivery_subzone_id").GetString(),
        ["place_id"] = locationAddress.GetProperty("place_id").GetString(),
        ["place_type"] = locationAddress.GetProperty("place_type").GetString(),
        ["address_id"] = locationAddress.GetProperty("address_id").GetString(),
        ["cell_details"] = new Dictionary<string, object?>
        {
            ["country_id"] = locationAddress.GetProperty("cell_details").GetProperty("country_id").GetInt32(),
            ["city_id"] = locationAddress.GetProperty("cell_details").GetProperty("city_id").GetInt32(),
            ["dsz_id"] = locationAddress.GetProperty("cell_details").GetProperty("dsz_id").GetInt32(),
            ["cell_id"] = locationAddress.GetProperty("cell_details").GetProperty("cell_id").GetString()
        }
    };

    Console.WriteLine($"\n📦 Fetching all restaurants near user location {locationAddress.GetProperty("full_name").GetString()}...");
    Console.WriteLine("=====================================================================================================================\n");
    result = await mcpClient.CallToolAsync(
        "get_all_restaurants",
        new Dictionary<string, object?>()
        {
            ["user_location"] = userLocation,
            ["page_size"] = 10,
            ["filters"] = null,
            ["postback_params"] = null
        },
        cancellationToken: CancellationToken.None
    );

    foreach (TextContentBlock block in result.Content.OfType<TextContentBlock>())
    {
        var restaurantsResult = JsonSerializer.Deserialize<RestaurantsResult>(block.Text);
        if (restaurantsResult?.results?.Count > 0)
        {
            var count = 1;
            foreach (var r in restaurantsResult.results)
            {
                Console.WriteLine($"Name: {r.name}");
                Console.WriteLine($"Rating: {r.rating} ({r.votes} votes)");
                Console.WriteLine($"Distance: {r.distance} km");
                Console.WriteLine($"ETA: {r.eta}");
                Console.WriteLine($"Image: {r.res_image}");
                Console.WriteLine($"Offer: {r.res_offer ?? "None"}");
                Console.WriteLine(new string('-', 40));
            }
        }
        else
        {
            Console.WriteLine("There are no restaurants found near this locaion in Zomato App.");
        }
    }


    //Console.WriteLine("\n✨ Client operations completed successfully!");
    Console.WriteLine("Press any key to close this window...");
    Console.ReadKey();
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error running MCP client: {ex.Message}");
    Console.WriteLine($"Stack trace: {ex.StackTrace}");
    Console.WriteLine("\nPress any key to continue...\n");
    Console.ReadKey();
}

public class Restaurant
{
    public int res_id { get; set; }
    public string? name { get; set; }
    public double rating { get; set; }
    public int votes { get; set; }
    public double distance { get; set; }
    public string? eta { get; set; }
    public string? res_image { get; set; }
    public string? res_offer { get; set; }
}

public class RestaurantsResult
{
    public List<Restaurant>? results { get; set; }
}

public class Cell_Details
{
    public int country_id { get; set; }
    public int city_id { get; set; }
    public int dsz_id { get; set; }
    public string? cell_id { get; set; }
}

public class Address
{
    public string? latitude { get; set; }
    public string? longitude { get; set; }
    public string? short_name { get; set; }
    public string? full_name { get; set; }
    public string? cell_id { get; set; }
    public string? delivery_subzone_id { get; set; }
    public string? place_id { get; set; }
    public string? place_type { get; set; }
    public string? address_id { get; set; }
    public Cell_Details? cell_details { get; set; }
}

public class AddressesResult
{
    public List<Address>? addresses { get; set; }
    public int count { get; set; }
    public bool success { get; set; }
}