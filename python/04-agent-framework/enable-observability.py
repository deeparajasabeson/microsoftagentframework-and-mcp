import asyncio
import os
from agent_framework.observability import setup_observability
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

# Api resources details
api_key = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"
endpoint = "https://agent-azureopenaiclient.openai.azure.com/"
deployment_name = "gpt-5-mini"


# Step 1: Basic setup - Enable observability with default settings

# Set the Azure region (any valid Azure region string, e.g., eastus)
import os
# os.environ["AZURE_MONITOR_SERVICE_REGION"] = "eastus"
os.environ["AZURE_MONITOR_STATSBEAT_REGION"] = "eastus"

# Step 2: Optionally suppress other noisy warnings like :: WARNING:azure.monitor.opentelemetry.exporter.statsbeat._manager:Exporter is missing a valid region.
os.environ["APPLICATIONINSIGHTS_STATSBEAT_DISABLED"] = "true"
# To supress warnings : 1) set environment variable or 2) execute the following 2 lines

# Step 3:Enable agent framework telemetry with console output (default behavior)
# Setup options-configure observability - Programmatic configuration:
setup_observability(
    enable_sensitive_data=True,
    otlp_endpoint="http://localhost:4317",
    applicationinsights_connection_string="InstrumentationKey=1f90218e-9383-445d-95df-1a01a987ea98"
)
print("Observability setup complete!")

async def main():
    # Create the agent - telemetry is automatically enabled
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name
        ),
        name="Joker",
        instructions="You are good at telling jokes."
    )

    # Run the agent
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)

# NOTE :: The console exporter will show trace data before display the result

if __name__ == "__main__":
    asyncio.run(main())
