// MSAL configuration
export const msalConfig = {
  auth: {
    clientId: process.env.REACT_APP_CLIENT_ID || "",
    authority: `https://login.microsoftonline.com/${process.env.REACT_APP_TENANT_ID}`,
    redirectUri: process.env.REACT_APP_REDIRECT_URI || "http://localhost:3000",
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
};

// Add scopes here for ID token to be used at Microsoft identity platform endpoints.
export const loginRequest = {
  scopes: ["User.Read"],
};

// Add the endpoints here for Microsoft Graph API services you'd like to use.
export const graphConfig = {
  graphMeEndpoint: "https://graph.microsoft.com/v1.0/me",
};

// Azure OpenAI and MCP configuration
export const apiConfig = {
  azureOpenAI: {
    endpoint: process.env.REACT_APP_AZURE_OPENAI_ENDPOINT || "",
    apiKey: process.env.REACT_APP_AZURE_OPENAI_API_KEY || "",
    deploymentName: process.env.REACT_APP_AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4.1",
    apiVersion: process.env.REACT_APP_AZURE_OPENAI_API_VERSION || "2024-02-01",
  },
  mcpServer: {
    url: process.env.REACT_APP_MCP_SERVER_URL || "",
    apiKey: process.env.REACT_APP_MCP_API_KEY || "",
  },
  agent: {
    name: process.env.REACT_APP_AGENT_NAME || "WeatherAgent",
    instructions: process.env.REACT_APP_AGENT_INSTRUCTIONS || "You are a helpful weather assistant.",
  },
};
