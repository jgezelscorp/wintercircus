using Microsoft.Extensions.Configuration;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.AzureAI;
using Microsoft.SemanticKernel.ChatCompletion;
using Azure.Identity;
using Azure;
using Azure.AI.Agents.Persistent;

var credential = new DefaultAzureCredential();

// Add configuration from appsettings.json, environment variables, and user secrets
var configBuilder = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables();

#if DEBUG
// For local development, add user secrets if available
configBuilder.AddUserSecrets<Program>();
#endif

var configuration = configBuilder.Build();

// Read config values (appsettings, env vars, or user secrets)
var openAiEndpoint = configuration["AzureOpenAI:Endpoint"] ?? throw new InvalidOperationException("AzureOpenAI:Endpoint is required");
var openAiApiKey = configuration["AzureOpenAI:ApiKey"] ?? throw new InvalidOperationException("AzureOpenAI:ApiKey is required");
var openAiDeployment = configuration["AzureOpenAI:DeploymentName"] ?? throw new InvalidOperationException("AzureOpenAI:DeploymentName is required");
var connectionString = configuration["ConnectionString"] ?? throw new InvalidOperationException("ConnectionString is required");
var stockExpertAgentId = configuration["Agents:StockExpertAgentId"] ?? throw new InvalidOperationException("Agents:StockExpertAgentId is required");
var investorAdvisorAgentId = configuration["Agents:InvestorAdvisorAgentId"] ?? throw new InvalidOperationException("Agents:InvestorAdvisorAgentId is required");

// Create Kernel
var builder = Kernel.CreateBuilder();
builder.Services.AddAzureOpenAIChatCompletion(
    deploymentName: openAiDeployment,
    endpoint: openAiEndpoint,
    apiKey: openAiApiKey
);
var kernel = builder.Build();

// Create Azure AI agents client using the correct Foundry GA endpoint pattern
var agentsClient = AzureAIAgent.CreateAgentsClient(connectionString, credential);

Console.WriteLine("🤖 Azure AI Foundry Agents Orchestrator with Semantic Kernel");
Console.WriteLine("============================================================");

Console.WriteLine("\n📋 Listing all available agents in your Azure AI Foundry project:");
try
{
    var availableAgents = agentsClient.Administration.GetAgentsAsync();
    bool foundAny = false;
    await foreach (var agent in availableAgents)
    {
        foundAny = true;
        Console.WriteLine($"   • Agent ID: {agent.Id}, Name: {agent.Name}, Model: {agent.Model}");
    }
    
    if (!foundAny)
    {
        Console.WriteLine("❌ No agents found in your Azure AI Foundry project.");
        Console.WriteLine("Please create agents in Azure AI Foundry portal first.");
        return;
    }
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error listing agents: {ex.Message}");
    return;
}

Console.WriteLine("\n🔍 Retrieving configured agents for orchestration...");

PersistentAgent stockExpertPersistentAgent;
PersistentAgent investorPersistentAgent;

try
{
    // Get the Azure AI agents from the Azure AI Foundry service using the correct GA pattern
    stockExpertPersistentAgent = await agentsClient.Administration.GetAgentAsync(stockExpertAgentId);
    Console.WriteLine($"   ✅ Successfully found Stock Expert agent: {stockExpertAgentId}");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error retrieving Stock Expert agent ({stockExpertAgentId}): {ex.Message}");
    return;
}

try
{
    investorPersistentAgent = await agentsClient.Administration.GetAgentAsync(investorAdvisorAgentId);
    Console.WriteLine($"   ✅ Successfully found Investor Advisor agent: {investorAdvisorAgentId}");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error retrieving Investor Advisor agent ({investorAdvisorAgentId}): {ex.Message}");
    return;
}

Console.WriteLine("\n🚀 Creating Semantic Kernel agent proxies and group chat...");

// Create proxy agents for Azure AI Foundry endpoints using Semantic Kernel
var stockExpertAgent = new AzureAIAgent(stockExpertPersistentAgent, agentsClient);
var investorAdvAgent = new AzureAIAgent(investorPersistentAgent, agentsClient);

// Create Semantic Kernel Agent group chat with both agents (use default settings)
var agentGroupChat = new AgentGroupChat(stockExpertAgent, investorAdvAgent);

Console.WriteLine("   ✅ Agent group chat created successfully!");

Console.WriteLine("\n💬 Starting conversation between agents...");
Console.WriteLine("=====================================");

// Start the interaction
agentGroupChat.AddChatMessage(new ChatMessageContent(AuthorRole.User, "Please discuss the current state of the stock market and provide investment advice for a conservative investor. The Stock Expert should analyze market trends, and the Investor Advisor should provide specific recommendations."));

// Process and display conversation messages asynchronously
int messageCount = 0;
await foreach (var content in agentGroupChat.InvokeAsync())
{
    messageCount++;
    string timestamp = DateTime.Now.ToString("HH:mm:ss");
    
    // Color-code based on agent role
    string roleColor = content.Role.ToString() switch
    {
        "User" => "🧑",
        "Assistant" => content.AuthorName?.Contains("Stock") == true ? "📈" : "💰",
        _ => "🤖"
    };
    
    Console.WriteLine($"\n[{timestamp}] {roleColor} {content.Role} ({content.AuthorName ?? "Unknown"}):");
    Console.WriteLine($"💭 {content.Content}");
    Console.WriteLine(new string('-', 80));
    
    // Limit to prevent infinite loops in demo
    if (messageCount >= 6)
    {
        Console.WriteLine("\n🏁 Conversation completed (limited to prevent infinite loop)");
        break;
    }
}

Console.WriteLine("\n✨ Azure AI Foundry agents orchestration complete!");
Console.WriteLine("Thank you for using Semantic Kernel with Azure AI Foundry! 🎉");