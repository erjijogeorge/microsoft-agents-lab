"""
Tutorial: Agent Run with Streaming

This tutorial demonstrates how to run an agent with streaming responses,
where the output is displayed incrementally as it's generated.

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
    Streaming agent sample.

    The agent will stream a list of update objects, and accessing the .text property
    on each update object provides the part of the text result contained in that update.
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
        instructions="You are good at telling stories.",
        name="Storyteller"
    )

    # Run the agent with streaming
    async for update in agent.run_stream("Tell me a story about pirates."):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line after streaming is complete


if __name__ == "__main__":
    asyncio.run(main())

