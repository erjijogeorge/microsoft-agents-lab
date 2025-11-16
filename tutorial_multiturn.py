"""
Tutorial: Multi-turn Conversations with an Agent

This tutorial demonstrates how to have multi-turn conversations with an agent,
where the agent maintains conversation history and context across multiple interactions.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/multi-turn-conversation

Key Concepts:
- Agents are stateless and don't maintain state internally
- Use AgentThread objects to hold conversation state
- Pass the thread to run() to maintain context between calls
- Multiple threads allow independent conversations with the same agent

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


async def basic_multiturn_conversation():
    """
    Basic multi-turn conversation example.
    
    The agent maintains conversation history through the thread object,
    allowing it to refer to previous messages when responding.
    """
    print("=" * 70)
    print("EXAMPLE 1: Basic Multi-turn Conversation")
    print("=" * 70)
    
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
    
    # Create a thread to hold the conversation state
    thread = agent.get_new_thread()
    
    # First turn - ask for a joke
    print("\n👤 User: Tell me a joke about a pirate.")
    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
    print(f"🤖 Agent: {result1.text}\n")
    
    # Second turn - modify the joke (agent remembers the previous joke)
    print("👤 User: Now add some emojis to the joke and tell it in the voice of a pirate's parrot.")
    result2 = await agent.run(
        "Now add some emojis to the joke and tell it in the voice of a pirate's parrot.",
        thread=thread
    )
    print(f"🤖 Agent: {result2.text}\n")


async def multiple_conversations():
    """
    Multiple independent conversations with the same agent.
    
    By creating multiple thread objects, you can have separate,
    independent conversations with the same agent instance.
    """
    print("=" * 70)
    print("EXAMPLE 2: Multiple Independent Conversations")
    print("=" * 70)
    
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
    
    # Create two separate threads for independent conversations
    thread1 = agent.get_new_thread()
    thread2 = agent.get_new_thread()
    
    # Conversation 1 - about pirates
    print("\n[CONVERSATION 1]")
    print("👤 User: Tell me a joke about a pirate.")
    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread1)
    print(f"🤖 Agent: {result1.text}\n")
    
    # Conversation 2 - about robots
    print("[CONVERSATION 2]")
    print("👤 User: Tell me a joke about a robot.")
    result2 = await agent.run("Tell me a joke about a robot.", thread=thread2)
    print(f"🤖 Agent: {result2.text}\n")
    
    # Continue conversation 1 - agent remembers the pirate joke
    print("[CONVERSATION 1 - continued]")
    print("👤 User: Now add some emojis to the joke and tell it in the voice of a pirate's parrot.")
    result3 = await agent.run(
        "Now add some emojis to the joke and tell it in the voice of a pirate's parrot.",
        thread=thread1
    )
    print(f"🤖 Agent: {result3.text}\n")
    
    # Continue conversation 2 - agent remembers the robot joke
    print("[CONVERSATION 2 - continued]")
    print("👤 User: Now add some emojis to the joke and tell it in the voice of a robot.")
    result4 = await agent.run(
        "Now add some emojis to the joke and tell it in the voice of a robot.",
        thread=thread2
    )
    print(f"🤖 Agent: {result4.text}\n")


async def main():
    """Run all multi-turn conversation examples."""
    await basic_multiturn_conversation()
    print("\n")
    await multiple_conversations()


if __name__ == "__main__":
    asyncio.run(main())

