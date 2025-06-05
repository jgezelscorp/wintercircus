//create new console program
dotnet new console

//paste code in program.cs

//install packages
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.Identity
dotnet add package Microsoft.SemanticKernel.Agents.Core --prerelease
dotnet add package Microsoft.SemanticKernel.Agents.AzureAI --prerelease
dotnet add package Microsoft.Extensions.Configuration
dotnet add package Microsoft.Extensions.Configuration.Json
dotnet add package Microsoft.SemanticKernel.Agents.Core --prerelease
dotnet add package Microsoft.SemanticKernel.Agents.AzureAI --prerelease
dotnet add package Azure.Identity
dotnet add package Azure.Core

//build and run
dotnet build
dotnet run