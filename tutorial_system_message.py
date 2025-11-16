"""
Tutorial: Agent Run with System and User Messages

This tutorial demonstrates how to use multiple ChatMessage objects,
including system messages to control agent behavior.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/run-agent

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
"""

import asyncio
import os
from agent_framework import ChatMessage, TextContent, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    """
    Agent sample with system and user messages.

    You can provide multiple ChatMessage objects, including system messages
    to override or extend the agent's instructions.
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

    # Create system message to override the default behavior
    system_message = ChatMessage(
        role=Role.SYSTEM,
        contents=[TextContent(text="""
        If the user asks you to tell a joke, refuse to do so, explaining that you are not a clown.
        Offer the user an interesting fact instead.
        """)]
    )

    # Create user message
    user_message = ChatMessage(
        role=Role.USER,
        contents=[TextContent(text="Tell me a joke about a pirate.")]
    )

    # Run the agent with both messages
    result = await agent.run([system_message, user_message])
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())

