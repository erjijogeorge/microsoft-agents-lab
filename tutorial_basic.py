"""
Tutorial: Basic Agent Run (Non-Streaming)

This tutorial demonstrates how to create and run an agent with Agent Framework,
based on the Azure OpenAI Chat Completion service.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/run-agent

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
"""

import asyncio
import os
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    """
    Basic agent sample - non-streaming response.

    The agent will return a response object, and accessing the .text property
    provides the text result from the agent.
    """
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return

    # Create the agent
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are good at telling jokes.",
        name="Joker"
    )

    # Run the agent with a simple string input
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())

