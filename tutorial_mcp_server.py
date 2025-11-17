"""
Tutorial: Exposing an Agent as an MCP Tool

This tutorial demonstrates how to expose an agent as a tool over the Model Context 
Protocol (MCP), so it can be used by other systems that support MCP tools.

From: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/agent-as-mcp-tool

Key Concepts:
- MCP (Model Context Protocol) allows agents to be exposed as tools
- Agents can be wrapped with as_mcp_server() to create an MCP server
- The server communicates over standard input/output (stdio)
- MCP-compatible clients (like VS Code GitHub Copilot) can use the agent as a tool

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable (e.g., https://your-resource.openai.azure.com)
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
- Install mcp and anyio packages: uv add mcp anyio
"""

import asyncio
import os
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import anyio
from mcp.server.stdio import stdio_server

# Load environment variables from .env file
load_dotenv()


def get_specials() -> Annotated[str, "Returns the specials from the menu."]:
    """Get the daily specials from the restaurant menu."""
    return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """


def get_item_price(
    menu_item: Annotated[str, "The name of the menu item."],
) -> Annotated[str, "Returns the price of the menu item."]:
    """Get the price of a menu item."""
    # In a real application, this would look up the price in a database
    return "$9.99"


async def run():
    """
    Main function to create and run the MCP server.
    
    This function:
    1. Creates an agent with tools (get_specials and get_item_price)
    2. Exposes the agent as an MCP server
    3. Runs the server over stdio (standard input/output)
    """
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        print("Error: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME in .env file")
        print("\nExample .env file:")
        print("AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com")
        print("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini")
        return
    
    print("=" * 70)
    print("MCP Server: Restaurant Agent")
    print("=" * 70)
    print(f"Using endpoint: {endpoint}")
    print(f"Using deployment: {deployment_name}")
    print("\nCreating agent with restaurant menu tools...")
    
    # Create an agent with tools
    agent = AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment_name,
        credential=AzureCliCredential()
    ).create_agent(
        name="RestaurantAgent",
        description="Answer questions about the menu.",
        tools=[get_specials, get_item_price],
    )
    
    print("Agent created successfully!")
    print("\nExposing agent as MCP server...")
    
    # Expose the agent as an MCP server
    server = agent.as_mcp_server()
    
    print("MCP server created!")
    print("\nStarting MCP server over stdio...")
    print("The server is now ready to accept requests from MCP clients.")
    print("(Press Ctrl+C to stop the server)")
    print("=" * 70)
    
    # Setup the MCP server to listen for incoming requests over stdio
    async def handle_stdin():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    await handle_stdin()


if __name__ == "__main__":
    anyio.run(run)

