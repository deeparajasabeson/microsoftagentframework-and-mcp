import os
import asyncio
from pathlib import Path

# Add references
from agent_framework import AgentThread, ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
from pydantic import Field
from typing import Annotated
import time
from typing import Optional
from azure.core.credentials import AccessToken

async def main():
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load the expnses data file
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # Ask for a prompt
    user_prompt = input(f"Here is the expenses data in your file:\n\n{data}\n\nWhat would you like me to do with it?\n\n")
    
    # Run the async agent code
    await process_expenses_data (user_prompt, data)

class StaticAsyncTokenCredential:
    """A custom credential that wraps a static key to implement the async get_token() method."""

    def __init__(self, key: str):
        self._key = key

    async def get_token(self, *scopes: str, **kwargs) -> AccessToken:
        """
        Returns the API key as the access token. 
        Note: The expiration time is set far in the future since API keys don't typically expire quickly.
        """
        # Return the key wrapped in an AccessToken object, required by Azure SDKs
        # Use a long-lived expiration time.
        expires_on = int(time.time()) + 3600  # Expires in 1 hour
        return AccessToken(self._key, expires_on)
    
async def process_expenses_data(prompt, expenses_data):
    # -----------------
    # 1. Define Variables and Custom Credential
    # -----------------
    AZURE_AI_PROJECT_ENDPOINT = "https://agent-azureopenaiclient.openai.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview"
    AZURE_AI_MODEL_DEPLOYMENT_NAME = "gpt-4.1-mini"
    DEPLOYMENT_API_KEY = "Ab2GlJUSQYwxHFUNul6TMIodpXDGxRM7jMCGywlvv2DcTiHwE1J0JQQJ99BJACYeBjFXJ3w3AAABACOG8QKg"

    # Create the credential object
    # This satisfies the framework's requirement for a credential with a get_token method
    async_key_credential = StaticAsyncTokenCredential(DEPLOYMENT_API_KEY)

    # -----------------
    # 2. Agent Initialization
    # -----------------
    async with (
        ChatAgent(
            chat_client=AzureAIAgentClient(
            # Pass the custom async credential object here
                            async_credential=DefaultAzureCredential(), 
                            endpoint=AZURE_AI_PROJECT_ENDPOINT,
                            model=AZURE_AI_MODEL_DEPLOYMENT_NAME
            ),
            name="expenses_agent",
            instructions="""You are an AI assistant for expense claim submission.
                            When a user submits expenses data and requests an expense claim, use the plug-in function to send an email to expenses@contoso.com with the subject 'Expense Claim`and a body that contains itemized expenses with a total.
                            Then confirm to the user that you've done so.""",
            tools=send_email,
        ) as agent,
    ):
        # Use the agent to process the expenses data
        try:
            # Add the input prompt to a list of messages to be submitted
            prompt_messages = [f"{prompt}: {expenses_data}"]
            # Invoke the agent for the specified thread with the messages
            response = await agent.run(prompt_messages)
            # Display the response
            print(f"\n# Agent:\n{response}")
        except Exception as e:
            # Something went wrong
            print (e)
   
# Create a tool function for the email functionality
def send_email(
 to: Annotated[str, Field(description="Who to send the email to")],
 subject: Annotated[str, Field(description="The subject of the email.")],
 body: Annotated[str, Field(description="The text body of the email.")]):
     print("\nTo:", to)
     print("Subject:", subject)
     print(body, "\n")


if __name__ == "__main__":
    asyncio.run(main())
