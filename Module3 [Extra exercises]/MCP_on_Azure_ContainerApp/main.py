"""
Azure Container App MCP Server

This FastAPI application serves as a Model Context Protocol (MCP) server that provides
weather information through Server-Sent Events (SSE) transport. It's designed to run
in Azure Container Apps and provides secure, API key-authenticated access to weather data.

Key Features:
- API key authentication for all endpoints
- SSE transport for real-time MCP communication
- Weather data access through MCP protocol
- Production-ready for Azure Container Apps deployment

Author: Generated for Azure Container Apps MCP Sample
"""

# Import necessary modules for FastAPI web server and MCP integration
from fastapi import FastAPI, Request, Depends
from mcp.server.sse import SseServerTransport  # Server-Sent Events transport for MCP
from starlette.routing import Mount
from weather import mcp  # Import the MCP server instance from weather module
from api_key_auth import ensure_valid_api_key  # Custom API key authentication middleware
import uvicorn  # ASGI server for running the FastAPI application

# Create FastAPI application instance
# - Disable documentation endpoints (docs_url=None, redoc_url=None) for security in production
# - Apply API key authentication globally to all routes via dependencies parameter
app = FastAPI(
    docs_url=None,  # Disable Swagger UI documentation endpoint
    redoc_url=None,  # Disable ReDoc documentation endpoint
    dependencies=[Depends(ensure_valid_api_key)]  # Require API key for all endpoints
)

# Initialize Server-Sent Events transport for MCP communication
# This handles the bidirectional communication between MCP clients and the server
# The "/messages/" path will be used for client-to-server message posting
sse = SseServerTransport("/messages/")

# Mount the SSE message handler at the /messages endpoint
# This allows MCP clients to send messages to the server via POST requests
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """
    Handle Server-Sent Events connections for MCP (Model Context Protocol) clients.
    
    This endpoint establishes a persistent SSE connection with MCP clients and runs
    the weather MCP server to handle client requests for weather information.
    
    The flow works as follows:
    1. Client connects to this SSE endpoint
    2. Server establishes bidirectional streams (read/write)
    3. MCP server initializes with default options
    4. Server runs the MCP protocol loop to handle client requests
    5. Weather tools (get_alerts, get_forecast) are made available to clients
    
    Args:
        request (Request): The incoming HTTP request object containing client connection info
        
    Returns:
        SSE stream: Persistent connection for MCP protocol communication
        
    Note:
        This endpoint requires valid API key authentication (handled by global dependency)
    """
    # Establish Server-Sent Events connection with the requesting client
    # This creates bidirectional streams for communication:
    # - read_stream: for receiving messages from the client
    # - write_stream: for sending messages to the client
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        # Get initialization options for the MCP server
        # This sets up the server with default configuration and available tools
        init_options = mcp._mcp_server.create_initialization_options()

        # Run the MCP server with the established streams
        # This starts the main protocol loop that will:
        # - Handle client initialization requests
        # - Process tool calls (weather alerts, forecasts)
        # - Manage the protocol lifecycle
        # - Continue until client disconnects
        await mcp._mcp_server.run(
            read_stream,  # Stream for reading client messages
            write_stream,  # Stream for sending responses to client
            init_options,  # Server initialization configuration
        )

# Application entry point
if __name__ == "__main__":
    """
    Start the FastAPI application using uvicorn ASGI server.
    
    Configuration:
    - host="0.0.0.0": Listen on all network interfaces (required for containers)
    - port=8000: Standard port for the application
    
    This makes the service accessible from:
    - Inside the container: http://localhost:8000
    - Outside the container: http://<container-ip>:8000
    - Azure Container Apps: https://<app-name>.<region>.azurecontainerapps.io
    
    Available endpoints:
    - GET /sse: Main MCP SSE endpoint for client connections
    - POST /messages: Message handling for MCP communication (auto-mounted)
    
    Security:
    - All endpoints require valid API key in x-api-key header
    - Documentation endpoints disabled for production security
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)