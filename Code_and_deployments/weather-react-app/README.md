# Weather React App

A React application with Entra ID authentication that provides an AI-powered weather assistant interface.

## Features

- 🔐 **Entra ID Authentication**: Secure login using Microsoft MSAL
- 🌤️ **Weather Agent Interface**: Chat-style interface similar to SK-Agent/main.py
- 🔗 **MCP Server Integration**: Connects to your Azure Container Instance weather server
- 💬 **Interactive Chat**: Real-time conversation with the weather agent
- 📊 **Usage Tracking**: Displays token usage and response metadata
- 🎨 **Modern UI**: Beautiful, responsive design with gradient backgrounds

## Prerequisites

1. **Entra ID App Registration**:
   - Create an app registration in Azure Portal
   - Set redirect URI to `http://localhost:3000`
   - Note down Client ID and Tenant ID

2. **Azure OpenAI**: Configured endpoint and API key
3. **MCP Weather Server**: Running on Azure Container Instance

## Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Configure Environment**:
   Update `.env` file with your values:
   ```env
   REACT_APP_CLIENT_ID=your-client-id-here
   REACT_APP_TENANT_ID=your-tenant-id-here
   REACT_APP_AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
   REACT_APP_AZURE_OPENAI_API_KEY=your-azure-openai-api-key
   REACT_APP_MCP_SERVER_URL=https://weather-mcp.nicepebble-f55fb74d.swedencentral.azurecontainerapps.io/sse
   REACT_APP_MCP_API_KEY=your-mcp-api-key
   ```

3. **Run the Application**:
   ```bash
   npm start
   ```

## How It Works

1. **Authentication Flow**:
   - User clicks "Sign in with Microsoft"
   - MSAL handles the Entra ID authentication
   - Upon successful login, the weather chat interface is displayed

2. **Weather Chat**:
   - Users can ask weather-related questions
   - The app simulates calling your MCP weather server
   - Responses include detailed weather information and metadata

3. **Features**:
   - Example questions for easy start
   - Real-time typing indicators
   - Error handling and user feedback
   - Session tracking and usage statistics

## Architecture

```
├── src/
│   ├── components/
│   │   ├── LoginButton.js      # Entra ID login component
│   │   └── WeatherChat.js      # Main chat interface
│   ├── authConfig.js           # MSAL and API configuration
│   ├── App.js                  # Main application component
│   ├── index.js               # React entry point
│   └── index.css              # Styling
├── public/
│   └── index.html             # HTML template
├── .env                       # Environment variables
└── package.json               # Dependencies and scripts
```

## Integration with MCP Server

The app is configured to connect to the same MCP weather server used by your SK-Agent:
- **Server URL**: `https://weather-mcp.nicepebble-f55fb74d.swedencentral.azurecontainerapps.io/sse`
- **Functions**: `get_forecast()`, `get_alerts()`
- **Authentication**: API key-based

## Security

- Uses MSAL for secure Entra ID authentication
- Environment variables for sensitive configuration
- Session-based token storage
- Proper logout handling

## Next Steps

To connect to your actual MCP server and Azure OpenAI:

1. Update the `simulateWeatherResponse` function in `WeatherChat.js`
2. Add actual HTTP requests to your Azure OpenAI endpoint
3. Implement proper MCP server communication
4. Add error handling for network requests

## Development

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
