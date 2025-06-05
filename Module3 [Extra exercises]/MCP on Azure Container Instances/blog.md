# Host remote MCP servers in Azure Container Apps

Whether you're building AI agents or using LLM powered tools like GitHub Copilot in Visual Studio Code, you're probably hearing a lot about [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) lately; maybe you're already using it. It's quickly becoming the standard interoperability layer between different components of the AI stack.

In this article, we'll explore how to run remote MCP servers as serverless containers in [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/overview) and use them in GitHub Copilot in Visual Studio Code.

## MCP servers today

MCP follows a client-server architecture. It all starts with a host, such as GitHub Copilot in VS Code or Claude Desktop. The host acts as a client and connects to one or more MCP servers.

Servers are the main extensibility points in MCP. Each server provides new tools, skills, and capabilities to the host. For example, a server can expose a search engine that allows an agent running in the host to search the web. Or the agent can use a GitHub MCP server to work with GitHub repositories. The possibilities are endless.

By default, most MCP servers run locally. The host starts each server as a subprocess and communicates with it using standard input and output. This works well for many scenarios. It's also safer from a security perspective because the server isn't exposed on a port and any secrets that the server needs remain local to the host.

## Remote MCP servers

As MCP matures, we're starting to see the community explore the idea of remote MCP servers. This is a natural evolution of the protocol. Instead of running a local MCP server that calls a search engine, imagine connecting to a large-scale, multi-tenant, remote MCP server in the cloud that's managed by the search engine provider.

MCP is still relatively in its early stages, and the community is still evolving the spec to support remote servers.

First, MCP needs to support a transport layer that allows the host to connect to a remote server. An HTTP with SSE (Server-Sent Events) transport layer was initially added, but the most recent spec is already deprecating it in favor of a [streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

And second, now that there are transports that allow remote servers, there now needs to be ways for clients to authenticate with remote servers. The spec in this area is still evolving as well.

## Building a remote MCP server

As of the time of this writing, clients are still catching up to the evolving spec. A client like VS Code already supports remote servers, but the current version only supports SSE transport and the only authentication method it works well with is API key headers.

We'll now deploy a remote MCP server using SSE transport and API key auth.

To follow along, clone the repo:

```bash
git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
```

We begin with the weather MCP server from the official quickstart (see `weather.py`). It exposes a simple tool for getting the weather in a given location in the United States. It runs locally and communicates with the host using standard input/output.

To add SSE transport, we add a FastAPI server (`main.py`).

```python
from fastapi import FastAPI, Request, Depends
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from weather import mcp


app = FastAPI(docs_url=None, redoc_url=None)

sse = SseServerTransport("/messages/")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        init_options = mcp._mcp_server.create_initialization_options()

        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            init_options,
        )
```

The MCP SDK already has a built-in SSE transport implementation. We just needed to add a FastAPI server that exposes the `/sse` endpoint and handles the `/messages` endpoint using the MCP SDK.

And to add API key authentication, we create a function that checks the `x-api-key` header in the request and compares it to a list of valid API keys. In more advanced scenarios, we could use a database or a secret management service to store the API keys and map them to individual users.

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="x-api-key")

def ensure_valid_api_key(api_key_header: str = Security(api_key_header)):
    def check_api_key(key: str) -> bool:
        valid_keys = os.environ.get("API_KEYS", "").split(",")
        return key in valid_keys and key != ""

    if not check_api_key(api_key_header):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
```

We can then add the `ensure_valid_api_key` function as a dependency so that it's required to call any route on the server.

```python
app = FastAPI(docs_url=None, redoc_url=None, dependencies=[Depends(ensure_valid_api_key)])
```

## Deploying the server to Azure Container Apps

Now let's deploy the server to Azure Container Apps.

Making sure we're in the root of the repo, we can run the following command to deploy the app along with all other necessary resources:

```bash
az containerapp up -g <RESOURCE_GROUP> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
```

It uses the Dockerfile in the repo to build the container image and deploy it to Azure Container Apps. The `--env-vars` flag sets the `API_KEYS` environment variable in the container. Provide a secure value. You can add multiple API keys by separating them with commas.

After the deployment is complete, the Azure CLI returns the URL of the app.

## Connecting to the server from Visual Studio Code

In VS Code, run the `MCP: Add server` command. Choose `HTTP (Server-sent events)` as the transport and enter the URL of the `/sse` endpoint on the server (for example, `https://weather-mcp.sleepypanda.westus.azurecontainerapps.io/sse`).

VS Code's `mcp.json` configuration file opens. Because the server requires an API key, make a couple of changes:

* Add a new `promptString` input for the API key. This will prompt you for the API key when you start the server.
* Add the `x-api-key` header to the server configuration. This will send the API key to the server when connecting.

```json
{
    "inputs": [
        {
            "type": "promptString",
            "id": "weather-api-key",
            "description": "Weather API Key",
            "password": true
        }
    ],
    "servers": {
        "weather-sse": {
            "type": "sse",
            "url": "https://weather-mcp.sleepypanda.westus.azurecontainerapps.io/sse",
            "headers": {
                "x-api-key": "${input:weather-api-key}"
            }
        }
    }
}
```

Next to the server in the JSON file, click the "Start" button. This initiates VS Code's connection to the server. You'll be prompted for the API key. Enter an API key you set in the `API_KEYS` environment variable when deploying the app.

Open the Copilot chat interface by typing `Ctrl+Shift+I` (`Cmd+Shift+I` on macOS). Change the mode to "Agent". Type "What's the weather in Seattle?" and press enter. The agent should use the MCP server and respond with the current weather in Seattle.

For more information on using MCP servers in VS Code, check out the [VS Code docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers).

## Conclusion

In this article, we explored how to run remote MCP servers in Azure Container Apps. We started with a simple weather MCP server and added SSE transport and API key authentication. We then deployed the server to Azure Container Apps and used it in GitHub Copilot in Visual Studio Code.

