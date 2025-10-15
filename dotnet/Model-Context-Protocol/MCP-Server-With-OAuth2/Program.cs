//This sample demonstrates how to create an MCP server that requires OAuth 2.0 authentication to access its tools and resources. The server provides weather-related tools protected by JWT bearer token authentication.

//The Protected MCP Server sample shows how to:

//Create an MCP server with OAuth 2.0 protection
//Configure JWT bearer token authentication
//Implement protected MCP tools and resources
//Integrate with ASP.NET Core authentication and authorization
//Provide OAuth resource metadata for client discovery

//This sample is useful for scenarios where you want to restrict access to your MCP server's tools and resources, ensuring that only authenticated users can utilize them.


//Need to install Test Auth O Server ::
//🔍 Options / Alternatives
//Use a mock OAuth / test OAuth server library
//There are open-source OAuth2 / OIDC mock servers you can run locally. For example, mock-oauth2-server (Kotlin) is intended for testing clients that depend on OAuth/OIDC. 
//GitHub
//You could run that as your “TestOAuthServer” and configure it to issue tokens your MCP / protected server will accept.

//git clone https://github.com/navikt/mock-oauth2-server.git
//cd mock-oauth2-server
//gradlew.bat build

//gradlew.bat run
//By default, it runs on http://localhost:8080 and provides a well-known configuration endpoint at http://localhost:8080/.well-known/openid-configuration
//You can configure your MCP server to trust tokens issued by this mock server.
//This approach allows you to test OAuth2 / OIDC flows without needing a full-fledged identity provider.

//TESTING :
//http://localhost:8080/.well-known/openid-configuration
//You should see JSON output — that means your mock OAuth server is running and can issue tokens.