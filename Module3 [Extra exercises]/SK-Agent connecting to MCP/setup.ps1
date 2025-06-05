# Setup script for Semantic Kernel Agent with MCP Weather Server

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Check if .env file exists and contains necessary variables
if (Test-Path ".env") {
    Write-Host ".env file found. Please make sure to update the following variables:" -ForegroundColor Yellow
    Write-Host "- AZURE_OPENAI_ENDPOINT" -ForegroundColor Cyan
    Write-Host "- AZURE_OPENAI_API_KEY" -ForegroundColor Cyan
    Write-Host "- AZURE_OPENAI_DEPLOYMENT_NAME" -ForegroundColor Cyan
    Write-Host "- MCP_API_KEY (if required by your MCP server)" -ForegroundColor Cyan
} else {
    Write-Host "Please create a .env file with your Azure OpenAI credentials" -ForegroundColor Red
}

Write-Host "`nSetup complete! Run 'python main.py' to start the agent." -ForegroundColor Green
