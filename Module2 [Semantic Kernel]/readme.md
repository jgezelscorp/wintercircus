# Module 2: Semantic Kernel Workshop

A hands-on workshop exploring Microsoft's Semantic Kernel framework for building intelligent AI applications. This workshop provides practical experience with real-world AI application patterns using Python and Azure OpenAI.

The original location of the workshop can be found [here](https://github.com/Azure-Samples/semantic-kernel-workshop/tree/main
)

## Workshop Overview

This workshop takes you from foundational concepts to advanced implementation patterns through a series of Jupyter notebooks and practical examples. You'll learn how to:

- Build AI applications using Microsoft's Semantic Kernel framework
- Create and orchestrate AI agents with different capabilities and roles
- Construct structured AI workflows using the Process Framework
- Implement enterprise-ready AI features with security and scalability in mind

### Pre-requirements

1. Add your Azure OpenAI credentials to the `.env` file:
   ```
   AZURE_OPENAI_ENDPOINT=https://xxxxxx.openai.azure.com/
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<deployment_name>
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002
   AZURE_OPENAI_API_KEY=xxxxxxxxxxx
   AZURE_OPENAI_API_VERSION=2025-03-01-preview
   ```

2. Start with the first notebook:
   - Begin with `01-intro-to-semantic-kernel/01-intro.ipynb`, which includes instructions for installing Semantic Kernel and other required packages.


## Workshop Modules

### 01. Introduction to Semantic Kernel

Learn the fundamentals of Semantic Kernel:
- Core architectural components (Kernel, AI Services, Plugins)
- Building semantic functions with prompts
- Creating native functions with Python code
- Enabling automatic function calling for AI agents

**Key Notebooks:**
- `01-intro.ipynb`: Core concepts, services, and function creation

### 02. Semantic Kernel Agents

Master the creation and orchestration of AI agents:
- Creating specialized agents with different personas
- Implementing multi-agent communication patterns
- Agent selection strategies and orchestration
- Building agent topologies for complex scenarios
- Integrating plugins with agents for enhanced capabilities

**Key Notebooks:**
- `02.1-agents.ipynb`: Creating and configuring agents
- `02.2-agents-chats.ipynb`: Inter-agent communication and complex patterns

### 03. Semantic Kernel with MCP

Learn to how to connect an SK Agent to MCP:
- Running your MCP server
- Using an Agent in Semantic Kernel to make calls to it

**Key Notebooks:**
- `03.1-sk-with-mcp.ipynb`: Semantic Kernel with MCP example

**Remark**
- `See Module3 [Extra Excercises]` for addition MCP Scenario's

### 04. Process Framework

Learn to build structured, event-driven AI workflows:
- Understanding the Process Framework architecture
- Defining events, steps, and state management
- Building conversational AI systems with processes
- Implementing complex business logic with AI capabilities
- Creating maintainable and testable AI workflows

**Key Notebooks:**
- `04.1-intro-to-processes.ipynb`: Building stateful, event-driven AI processes

## Project Structure

```
Module2 [Semantic Kernel]
├── 01-intro-to-semantic-kernel/    # Introduction to core concepts
│   └── 01-intro.ipynb              # Basic concepts and functions
├── 02-semantic-kernel-agents/      # Agent creation and orchestration
│   ├── 02.1-single-agents.ipynb    # Agent fundamentals
│   ├── 02.2-agents-chats.ipynb     # Multi-agent communication
├── 03-semantic-kernel-mcp/         # Using SK with MCP
│   └── 03.1-sk-with-mcp.ipynb      # SK + MCP example
├── 04-process-framework/           # Structured AI workflows
│   └── 04.1-intro-to-processes.ipynb  # Process fundamentals
├── playground/                     # Interactive application
│   ├── backend/                    # FastAPI server
│   ├── frontend/                   # React application
│   ├── start.sh                    # Launch script
│   └── README.md                   # Playground documentation
└── .env.example                 # Environment variables template
```

## Learning Path

For optimal learning, follow the repository's folders in numerical order.

## Advanced Topics and Resources

For advanced patterns and enterprise deployment scenarios, explore the [Semantic Kernel Advanced Usage](https://github.com/Azure-Samples/semantic-kernel-advanced-usage) repository, which includes:

- Dapr integration for scalable, distributed systems
- Authentication and security patterns
- Natural language to SQL conversion
- Copilot Studio integration
- Microsoft Graph API integration
- Production deployment architecture

## Additional Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
- [Microsoft Copilot Studio](https://www.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-studio)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
