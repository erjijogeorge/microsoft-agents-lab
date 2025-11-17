"""
Tutorial: Exposing an Agent as an MCP Tool over HTTP

This tutorial demonstrates how to expose an agent as a tool over HTTP using
the Model Context Protocol (MCP) with Server-Sent Events (SSE).

Key Concepts:
- MCP server exposed over HTTP instead of stdio
- Uses SSE (Server-Sent Events) for streaming responses
- Accessible via HTTP port (default: 8000)
- Can be tested with HTTP clients or MCP clients that support HTTP transport

Prerequisites:
- Set AZURE_OPENAI_ENDPOINT environment variable
- Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable
- Run 'az login' to authenticate with Azure CLI
- Install dependencies: uv add mcp anyio uvicorn
"""

import os
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import uvicorn
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response

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
    return "$9.99"


# Global instances
mcp_server = None
sse_transport = None


async def handle_sse(request):
    """Handle SSE connections for MCP."""
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )
    # Return empty response to avoid NoneType error
    return Response()


def create_app():
    """Create the Starlette application with MCP server."""
    global mcp_server, sse_transport

    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        raise ValueError(
            "Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME "
            "environment variables"
        )

    print("=" * 70)
    print("MCP Server: Restaurant Agent (HTTP/SSE)")
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

    print("✓ Agent created successfully!")
    print("\nExposing agent as MCP server...")

    # Expose the agent as an MCP server
    mcp_server = agent.as_mcp_server()

    print("✓ MCP server created!")

    # Create SSE transport
    sse_transport = SseServerTransport("/messages/")

    # Create Starlette app with SSE endpoint
    app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=sse_transport.handle_post_message),
        ]
    )

    return app


def main():
    """Run the HTTP MCP server."""
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    host = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
    
    print("\n" + "=" * 70)
    print(f"Starting MCP server on http://{host}:{port}")
    print("=" * 70)
    print(f"\nEndpoints:")
    print(f"  - SSE: http://{host}:{port}/sse")
    print(f"  - Messages: http://{host}:{port}/messages")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    app = create_app()
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    main()

