# Semantic Kernel Weather Agent

This project creates a Semantic Kernel agent that connects to an MCP (Model Context Protocol) weather server running on Azure Container Instance. The agent uses Azure OpenAI GPT-4.1 to provide intelligent weather information.

## Setup

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   
   Update the `.env` file with your Azure OpenAI credentials:
   
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=your-gpt4-deployment-name
   AZURE_OPENAI_API_VERSION=2024-02-01
   
   # MCP Server Configuration (already configured)
   MCP_SERVER_URL=https://weather-mcp.nicepebble-f55fb74d.swedencentral.azurecontainerapps.io/sse
   MCP_API_KEY=your-mcp-api-key-if-required
   
   # Agent Configuration (optional - defaults provided)
   AGENT_NAME=WeatherAgent
   AGENT_INSTRUCTIONS=You are a helpful weather assistant that can provide weather forecasts and alerts for any location.
   ```

3. **Run the Agent**
   ```powershell
   python main.py
   ```

## Features

The agent can:
- Get weather forecasts for any location (requires latitude/longitude)
- Retrieve weather alerts for US states
- Provide detailed weather information using the National Weather Service API

## Available MCP Tools

The weather MCP server provides these tools:
- `get_forecast(latitude, longitude)` - Get weather forecast for a location
- `get_alerts(state)` - Get weather alerts for a US state (2-letter code)

## Example Queries

The current code includes these example queries:
1. Weather forecast for Seattle
2. Weather alerts for Washington state  
3. Weather forecast for New York City

You can modify the `USER_INPUTS` list in `main.py` to test different queries.

## Azure Foundry GPT-4.1 Configuration

Make sure your Azure OpenAI deployment is using GPT-4.1 (or GPT-4 Turbo) model and update the `AZURE_OPENAI_DEPLOYMENT_NAME` in your `.env` file accordingly.
