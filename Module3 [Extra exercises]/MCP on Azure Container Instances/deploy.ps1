# Deploys the Azure Container App for the weather MCP
# Run from root of the repository

# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"


# Azure Authentication Section
Write-Host "Authenticating with Azure..."
try {
    # Simple check if already logged in - avoid using jobs which can cause issues
    Write-Host "Checking Azure login status..."
    $loginCheck = az account list --output json 2>$null
    
    if ($loginCheck -and $loginCheck -ne "[]") {
        # Parse the JSON to get the account name
        $accounts = $loginCheck | ConvertFrom-Json
        $currentAccount = $accounts | Where-Object { $_.isDefault -eq $true }
        
        if ($currentAccount) {
            Write-Host "Already logged in as: $($currentAccount.name) (Subscription: $($currentAccount.id))"
        } else {
            Write-Host "No default account found. Starting login process..."
            # Use interactive login
            az login
        }
    } else {
        # Not logged in, prompt for login
        Write-Host "Not logged in. Please log in to your Azure account..."
        az login
    }
    
    # Verify login was successful
    $currentAccount = (az account show --output json 2>$null) | ConvertFrom-Json
    if ($currentAccount) {
        Write-Host "Active subscription: $($currentAccount.name) (ID: $($currentAccount.id))"
    } else {
        Write-Host "Failed to verify Azure login. Please run 'az login' manually and try again."
        exit 1
    }
} catch {
    Write-Host "Error during Azure authentication: $_"
    Write-Host "Please run 'az login' manually and try the script again."
    exit 1
}

# Set Azure subscription if needed
# Uncomment and update if you need to set a specific subscription
# $subscriptionId = "your-subscription-id"
# Write-Host "Setting Azure subscription to: $subscriptionId"
# az account set --subscription $subscriptionId

# Load deployment environment variables
. "$PSScriptRoot/.env.deploy.ps1"

# Check if resource group exists, create if it doesn't
Write-Host "Checking if resource group $RG exists..."
try {
    $rgExists = az group exists -n $RG
    if ($rgExists -eq "false") {
        Write-Host "Resource group $RG does not exist. Creating..."
        az group create --name $RG --location $LOCATION --output none
        
        if ($?) {
            Write-Host "Resource group created successfully." -ForegroundColor Green
        } else {
            Write-Host "Failed to create resource group. Please check errors above." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Resource group $RG already exists." -ForegroundColor Green
    }
} catch {
    Write-Host "Error checking resource group: $_" -ForegroundColor Red
    exit 1
}

# Check if Container Apps environment exists
Write-Host ""
Write-Host "Checking if Container Apps environment exists..."
try {
    $envExists = az containerapp env list --resource-group $RG --query "[?name=='$ENVIRONMENT_NAME'].name" -o tsv 2>$null
    
    if (-not $envExists) {
        Write-Host "Creating Container Apps environment: $ENVIRONMENT_NAME"
        Write-Host "This may take several minutes..."
        
        az containerapp env create --name $ENVIRONMENT_NAME --resource-group $RG --location $LOCATION --output none
        
        if ($?) {
            Write-Host "Container Apps environment created successfully." -ForegroundColor Green
        } else {
            Write-Host "Failed to create Container Apps environment. Please check errors above." -ForegroundColor Red
            Write-Host "Continuing anyway in case the environment exists but couldn't be detected properly..."
        }
    } else {
        Write-Host "Container Apps environment $ENVIRONMENT_NAME already exists." -ForegroundColor Green
    }
} catch {
    Write-Host "Error checking Container Apps environment: $_" -ForegroundColor Red
    Write-Host "Will attempt to continue anyway in case the environment exists..."
}

# Deploy the container app
Write-Host "Deploying Azure Container App to resource group: $RG"
Write-Host "This may take several minutes..."
Write-Host ""
Write-Host "Command: az containerapp up -g $RG -n $CONTAINER_APP_NAME --environment $ENVIRONMENT_NAME -l $LOCATION --env-vars API_KEYS=$APIKEYS --source ."
Write-Host ""

try {
    # Execute the deployment directly instead of using Start-Process
    # This ensures proper output and error handling
    az containerapp up -g $RG -n $CONTAINER_APP_NAME --environment $ENVIRONMENT_NAME -l $LOCATION --env-vars API_KEYS=$APIKEYS --source .
    
    # Check deployment status
    $deploymentStatus = $?
    if ($deploymentStatus) {
        Write-Host ""
        Write-Host "Deployment completed successfully." -ForegroundColor Green
        
        # Get the app URL
        Write-Host "Retrieving application URL..."
        $appUrl = az containerapp show -n $CONTAINER_APP_NAME -g $RG --query "properties.configuration.ingress.fqdn" -o tsv
        if ($appUrl) {
            Write-Host "Application is available at: https://$appUrl" -ForegroundColor Cyan
        } else {
            Write-Host "Could not retrieve application URL. You can check it in the Azure portal."
        }
    } else {
        Write-Host ""
        Write-Host "Deployment may have encountered issues. Please check the output above for errors." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error during deployment: $_" -ForegroundColor Red
    Write-Host "You can try deploying manually using:" -ForegroundColor Yellow
    Write-Host "az containerapp up -g $RG -n $CONTAINER_APP_NAME --environment $ENVIRONMENT_NAME -l $LOCATION --env-vars API_KEYS=$APIKEYS --source ." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Deployment script completed." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you encountered any issues, please check:"
Write-Host "1. Azure CLI installation: az --version"
Write-Host "2. Azure login status: az account show"
Write-Host "3. Resource group status: az group show -n $RG"
Write-Host "4. Container App status: az containerapp show -n $CONTAINER_APP_NAME -g $RG"
Write-Host ""