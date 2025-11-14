import asyncio
import os
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    """
    Basic agent sample using Microsoft Agent Framework.

    This demonstrates how to create and use a simple AI agent with Azure AI
    as the backend using ChatAgent with AzureAIAgentClient.

    Prerequisites:
    - Set AZURE_AI_PROJECT_ENDPOINT environment variable
    - Set AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable
    - Run 'az login' to authenticate with Azure CLI
    """
    # Get environment variables
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    print(" ")
    print("***********************************************************************")
    print(" ")


    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling stories."
        ) as agent,
    ):
        result = await agent.run("Tell me a story about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
