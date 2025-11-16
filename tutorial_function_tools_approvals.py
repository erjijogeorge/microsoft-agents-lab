"""
Tutorial: Using Function Tools with Human-in-the-Loop Approvals

This tutorial demonstrates how to use function tools that require human approval
before execution. This is useful for sensitive operations that need user confirmation.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/function-tools-approvals

Key Concepts:
- Human-in-the-loop pattern requires user input before executing certain functions
- Use approval_mode="always_require" in the @ai_function decorator
- Check for user_input_requests in the agent response
- Create approval responses using create_response() method
- Handle multiple approvals in a loop for complex scenarios

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
"""

import asyncio
import os
from typing import Annotated
from agent_framework import ai_function, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Function that does NOT require approval
@ai_function
def get_weather(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


# Function that REQUIRES approval before execution
@ai_function(approval_mode="always_require")
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get detailed weather information for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C, humidity 88%, wind 10 km/h."


async def simple_approval_example():
    """
    Example 1: Simple function approval
    
    This example shows how to handle a single function call that requires approval.
    """
    print("=" * 70)
    print("EXAMPLE 1: Simple Function Approval")
    print("=" * 70)
    
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return
    
    # Create the agent with both functions
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are a helpful weather assistant.",
        name="WeatherAgent",
        tools=[get_weather, get_weather_detail]
    )
    
    # Ask for detailed weather (which requires approval)
    print("\n👤 User: What is the detailed weather like in Amsterdam?")
    result = await agent.run("What is the detailed weather like in Amsterdam?")
    
    # Check if there are any approval requests
    if result.user_input_requests:
        print("\n⚠️  Approval Required!")
        
        for user_input_needed in result.user_input_requests:
            print(f"   Function: {user_input_needed.function_call.name}")
            print(f"   Arguments: {user_input_needed.function_call.arguments}")
            
            # Simulate user approval (in a real app, this would be interactive)
            user_approval = input("\n   Approve this function call? (yes/no): ").lower() == "yes"
            
            # Create the approval response
            approval_message = ChatMessage(
                role=Role.USER,
                contents=[user_input_needed.create_response(user_approval)]
            )
            
            # Continue the conversation with the approval
            final_result = await agent.run([
                "What is the detailed weather like in Amsterdam?",
                ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]),
                approval_message
            ])
            
            print(f"\n🤖 Agent: {final_result.text}\n")
    else:
        print(f"\n🤖 Agent: {result.text}\n")


async def handle_approvals(query: str, agent) -> str:
    """
    Helper function to handle function call approvals in a loop.
    
    This handles multiple function calls that may require approval,
    continuing until all approvals are processed and a final result is obtained.
    """
    current_input = query
    
    while True:
        result = await agent.run(current_input)
        print("Result: ", result.user_input_requests)
        
        if not result.user_input_requests:
            # No more approvals needed, return the final result
            return result.text
        
        # Build new input with all context
        new_inputs = [query]
        
        for user_input_needed in result.user_input_requests:
            print(f"\n⚠️  Approval needed for: {user_input_needed.function_call.name}")
            print(f"   Arguments: {user_input_needed.function_call.arguments}")
            
            # Add the assistant message with the approval request
            new_inputs.append(ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]))
            
            # Get user approval (in practice, this would be interactive)
            user_approval = input("   Approve this function call? (yes/no): ").lower() == "yes"
            
            # Add the user's approval response
            new_inputs.append(
                ChatMessage(role=Role.USER, contents=[user_input_needed.create_response(user_approval)])
            )
        
        # Continue with all the context
        current_input = new_inputs


async def multiple_approvals_example():
    """
    Example 2: Multiple function approvals in a loop

    This example shows how to handle multiple function calls that require approval
    using a helper function that loops until all approvals are processed.
    """
    print("=" * 70)
    print("EXAMPLE 2: Multiple Function Approvals")
    print("=" * 70)

    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        return

    # Create the agent with both functions
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        instructions="You are a helpful weather assistant.",
        name="WeatherAgent",
        tools=[get_weather, get_weather_detail]
    )

    # Ask for detailed weather for multiple cities
    print("\n👤 User: Get detailed weather for Seattle and Portland")
    result_text = await handle_approvals("Get detailed weather for Seattle and Portland", agent)
    print(f"\n🤖 Agent: {result_text}\n")


async def main():
    """Run all function approval examples."""
    print("\nThis tutorial demonstrates human-in-the-loop approvals for function calls.")
    print("You'll be prompted to approve or reject function calls.\n")

    await simple_approval_example()
    print("\n")
    await multiple_approvals_example()


if __name__ == "__main__":
    asyncio.run(main())

