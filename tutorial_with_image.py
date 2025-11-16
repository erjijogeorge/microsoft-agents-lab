"""
Tutorial: Agent Run with ChatMessage and Image

This tutorial demonstrates how to use ChatMessage objects with the agent,
including sending images for analysis.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/run-agent

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable (must support vision, e.g., gpt-4o)
- Run 'az login' to authenticate with Azure CLI
"""

import asyncio
import os
from agent_framework import ChatMessage, TextContent, UriContent, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    """
    Agent sample with ChatMessage containing text and image.

    Instead of a simple string, you can provide ChatMessage objects with
    multiple content types including images.
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

    # Create a message with text and image content
    message = ChatMessage(
        role=Role.USER,
        contents=[
            TextContent(text="Tell me a joke about this image?"),
            UriContent(
                uri="https://upload.wikimedia.org/wikipedia/commons/1/11/Joseph_Grimaldi.jpg",
                media_type="image/jpeg"
            )
        ]
    )

    # Run the agent with the ChatMessage
    result = await agent.run(message)
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())

