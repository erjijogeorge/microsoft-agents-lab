"""
Tutorial: Using Function Tools with an Agent

This tutorial demonstrates how to use function tools with an agent, where the agent
can call custom Python functions when needed to accomplish tasks.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/function-tools

Key Concepts:
- Function tools are custom code that the agent can call when needed
- Use type annotations with Annotated and Pydantic's Field to provide descriptions
- You can use the @ai_function decorator to explicitly specify function metadata
- Multiple related functions can be organized in a class

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
"""

import asyncio
import os
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ai_function
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


async def simple_function_tool():
    """
    Example 1: Simple function tool
    
    This example shows how to create a simple function tool that the agent
    can call when needed. The function uses type annotations to provide
    descriptions to the agent.
    """
    print("=" * 70)
    print("EXAMPLE 1: Simple Function Tool")
    print("=" * 70)
    
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return
    
    # Create the agent with the function tool
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are a helpful assistant",
        tools=get_weather
    )
    
    # Run the agent - it will automatically call the get_weather function
    print("\n👤 User: What is the weather like in Amsterdam?")
    result = await agent.run("What is the weather like in Amsterdam?")
    print(f"🤖 Agent: {result.text}\n")


@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather_with_decorator(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location using the ai_function decorator."""
    return f"The weather in {location} is cloudy with a high of 15°C."


async def function_tool_with_decorator():
    """
    Example 2: Function tool with @ai_function decorator
    
    This example shows how to use the @ai_function decorator to explicitly
    specify the function's name and description.
    """
    print("=" * 70)
    print("EXAMPLE 2: Function Tool with @ai_function Decorator")
    print("=" * 70)
    
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return
    
    # Create the agent with the decorated function tool
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are a helpful assistant",
        tools=get_weather_with_decorator
    )
    
    # Run the agent
    print("\n👤 User: What is the weather like in Paris?")
    result = await agent.run("What is the weather like in Paris?")
    print(f"🤖 Agent: {result.text}\n")


class WeatherTools:
    """A class containing multiple related function tools."""
    
    def __init__(self):
        self.last_location = None
    
    def get_weather(
        self,
        location: Annotated[str, Field(description="The location to get the weather for.")],
    ) -> str:
        """Get the weather for a given location."""
        self.last_location = location
        return f"The weather in {location} is cloudy with a high of 15°C."
    
    def get_weather_details(self) -> str:
        """Get the detailed weather for the last requested location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detailed weather in {self.last_location} is cloudy with a high of 15°C, low of 7°C, and 60% humidity."


async def class_with_multiple_tools():
    """
    Example 3: Class with multiple function tools

    This example shows how to organize related functions in a class,
    which can be useful for sharing state between functions.
    """
    print("=" * 70)
    print("EXAMPLE 3: Class with Multiple Function Tools")
    print("=" * 70)

    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return

    # Create an instance of the tools class
    tools = WeatherTools()

    # Create the agent with multiple function tools from the class
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are a helpful assistant",
        tools=[tools.get_weather, tools.get_weather_details]
    )

    # First request - get basic weather
    print("\n👤 User: What is the weather like in Tokyo?")
    result1 = await agent.run("What is the weather like in Tokyo?")
    print(f"🤖 Agent: {result1.text}\n")

    # Second request - get detailed weather (uses state from previous call)
    print("👤 User: Can you give me more details about the weather?")
    result2 = await agent.run("Can you give me more details about the weather?")
    print(f"🤖 Agent: {result2.text}\n")


async def main():
    """Run all function tool examples."""
    await simple_function_tool()
    print("\n")
    await function_tool_with_decorator()
    print("\n")
    await class_with_multiple_tools()


if __name__ == "__main__":
    asyncio.run(main())

