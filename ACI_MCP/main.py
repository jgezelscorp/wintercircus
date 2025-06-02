"""
Azure Container Apps MCP Server

This module implements a FastAPI web server that hosts a Model Context Protocol (MCP)
server for weather information. The server provides:

1. API key authentication for all endpoints
2. Server-Sent Events (SSE) transport for MCP communication
3. Weather data access through the MCP protocol

The server is designed to run in Azure Container Apps and provides a secure,
scalable way to expose weather functionality to MCP clients.

Key Components:
- FastAPI application with security middleware
- SSE transport for real-time MCP communication
- Weather MCP server integration
- API key-based authentication

Endpoints:
- GET /sse: Main SSE endpoint for MCP client connections
- POST /messages: Message handling for MCP communication

Author: Generated for Azure Container Apps MCP Sample
"""

# Import necessary libraries for the FastAPI web server and MCP integration
from fastapi import FastAPI, Request, Depends
from mcp.server.sse import SseServerTransport  # Server-Sent Events transport for MCP
from starlette.routing import Mount
from weather import mcp  # Import the MCP server instance from weather module
from api_key_auth import ensure_valid_api_key  # Custom API key authentication
import uvicorn  # ASGI server for running the FastAPI application

# Create FastAPI application instance
# - Disable auto-generated documentation endpoints for security
# - Apply API key authentication to all routes by default
app = FastAPI(docs_url=None, redoc_url=None, dependencies=[Depends(ensure_valid_api_key)])

# Initialize Server-Sent Events transport for MCP communication
# This handles the bidirectional communication between MCP clients and the server
sse = SseServerTransport("/messages/")

# Mount the SSE message handler at the /messages endpoint
# This allows MCP clients to send messages to the server
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

# Define the main SSE endpoint for MCP client connections
@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """
    Handle Server-Sent Events connections for MCP (Model Context Protocol) clients.
    
    This endpoint establishes a persistent connection with MCP clients and runs
    the weather MCP server to handle client requests for weather information.
    
    Args:
        request: The incoming HTTP request object
        
    Returns:
        SSE stream connection for MCP communication
    """
    # Establish SSE connection with the client
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        # Get initialization options for the MCP server
        init_options = mcp._mcp_server.create_initialization_options()

        # Run the MCP server with the established streams
        # This will handle all MCP protocol communication and weather requests
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            init_options,
        )# Application entry point
# Run the FastAPI application using uvicorn ASGI server when executed directly
if __name__ == "__main__":
    # Start the server on all interfaces (0.0.0.0) at port 8000
    # This makes the service accessible from outside the container/host
    uvicorn.run(app, host="0.0.0.0", port=8000)