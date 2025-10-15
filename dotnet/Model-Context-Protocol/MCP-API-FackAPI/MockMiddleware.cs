using System.Text.Json.Nodes;

public static class RouteMiddlewareExtensions
{
    public static WebApplication UseExtraRoutes(this WebApplication app)
    {
        var mockData = JsonNode.Parse(File.ReadAllText("mock.json"));

        // Fix: Check for null before dereferencing mockData or its Root
        if (mockData?.Root is not JsonObject rootObj)
        {
            // Optionally, you could throw or log here if mockData is not as expected
            return app;
        }

        foreach (var elem in rootObj)
        {
            if (elem.Value == null) continue;
            var array = elem.Value?.AsArray();
            // GET all items

            app.MapGet($"/{elem.Key}", () => elem.Value?.ToString());
            // GET item by ID
            app.MapGet($"/{elem.Key}/{{id}}", (int id) =>
            {
                if (array == null) return null;
                var item = array.SingleOrDefault(row =>
                    row != null &&
                    row.AsObject() != null &&
                    row.AsObject().Any(o => o.Key == "Id" && int.Parse(o.Value?.ToString() ?? "0") == id));
                return item;
            });
            // POST new item
            app.MapPost($"/{elem.Key}", async (HttpRequest request) =>
            {
                if (array == null) return null;
                app.MapGet($"/{elem.Key}", () => elem.Value != null ? elem.Value.ToString() : string.Empty);
                using StreamReader reader = new StreamReader(request.Body);
                var content = await reader.ReadToEndAsync();
                var newItem = JsonNode.Parse(content);
                if (newItem != null)
                {
                    newItem["Id"] = array.Count + 1;
                    array.Add(newItem);
                    File.WriteAllText("mock.json", mockData.ToString());
                }
                return newItem;
            });
            // DELETE item by ID
            app.MapDelete($"/{elem.Key}/{{id}}", (int id) =>
            {
                if (array == null) return "Deleted";
                var item = array.SingleOrDefault(row =>
                    row != null &&
                    row.AsObject() != null &&
                    row.AsObject()!.Any(o => o.Key == "Id" && o.Value != null && int.Parse(o.Value.ToString() ?? "0") == id));
                if (item != null)
                {
                    array.Remove(item);
                    File.WriteAllText("mock.json", mockData.ToString());
                }
                return "Deleted";
            });
        }
        return app;
    }
}