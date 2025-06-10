# 🔧 Environment Setup Guide

This guide will help you set up all the necessary environment variables for the three projects in this repository.

## 📁 Projects Overview

1. **ACI_MCP** - Azure Container Apps MCP server for weather data
2. **SK-Agent** - Semantic Kernel agent that uses Azure OpenAI and the above MCP server
3. **weather-react-app** - React web application with Azure AD auth and weather features  


## 🚀 Quick Setup

### Step 1: Copy Template Files

Copy the `.env.template` files to `.env` files in each project:

```powershell
# For SK-Agent
Copy-Item "SK-Agent\.env.template" "SK-Agent\.env"

# For weather-react-app  
Copy-Item "weather-react-app\.env.template" "weather-react-app\.env"

# For ACI_MCP
Copy-Item "ACI_MCP\.env.template" "ACI_MCP\.env"
```

### Step 2: Get Required Azure Resources

You'll need these Azure resources:

#### 🧠 Azure OpenAI Service
* You can reuse the resources you have deployed earlier today

#### 🔐 Azure Active Directory App Registration (for React app)
1. Go to Azure Portal > Entra ID > App registrations
2. Create a new registration (Single Tenant)
3. Set redirect URI to `http://localhost:3000` (for development)
4. Copy the Application (client) ID and Directory (tenant) ID

#### 🌤️ MCP Server Deployment (optional - you can use a public one)
1. Deploy the ACI_MCP project to Azure Container Apps
2. Get the URL of your deployed container app
3. Set up API keys for authentication

### 🛠️ Configuration Steps

#### For SK-Agent (.env):
```bash
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01
MCP_SERVER_URL=https://your-weather-mcp-server.azurecontainerapps.io/sse
MCP_API_KEY=your_mcp_server_api_key_here
```

#### For weather-react-app (.env):
```bash
REACT_APP_CLIENT_ID=your_azure_ad_client_id_here
REACT_APP_TENANT_ID=your_azure_ad_tenant_id_here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
REACT_APP_AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
REACT_APP_AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
REACT_APP_MCP_SERVER_URL=https://your-weather-mcp-server.azurecontainerapps.io/sse
REACT_APP_MCP_API_KEY=your_mcp_server_api_key_here
```

#### For ACI_MCP (.env):
```bash
API_KEYS=your_api_key_1,your_api_key_2,your_api_key_3
```

## 🔄 Testing Your Setup

### Test SK-Agent:
```powershell
cd SK-Agent
python main.py
```

### Test React App:
```powershell
cd weather-react-app
npm start
```

### Test MCP Server:
```powershell
cd ACI_MCP
python main.py
```

## 🚨 Troubleshooting

### Common Issues:

#### "Missing required environment variables"
- Check that your .env file exists and has all required variables
- Ensure no extra spaces around the `=` sign
- Verify file is named exactly `.env` (not `.env.txt`)

#### Azure OpenAI "Unauthorized"
- Verify your API key is correct
- Check that your endpoint URL ends with `/`
- Ensure your deployment name matches exactly

#### MCP Server Connection Failed
- Verify the MCP server URL is accessible
- Check that API key matches what's configured on server
- Test the URL in a browser (should return some response)
- URL ends like ***/sse***

#### React App Auth Issues
- Verify Client ID and Tenant ID are correct
- Check redirect URI matches your app registration
- Ensure localhost:3000 is added as a redirect URI
- Make sure to 'configure' CORS to allow all *  

## 📞 Getting Help

If you need help:
1. Check the individual project README files
2. Verify all environment variables are set correctly
3. Test each component individually
4. Check Azure portal for resource status
5. Ask

---

🎉 **You're all set!** Once configured, you'll have a complete weather assistant system with:
- AI-powered conversational interface
- Real-time weather data
- Secure authentication  
- Scalable cloud deployment
