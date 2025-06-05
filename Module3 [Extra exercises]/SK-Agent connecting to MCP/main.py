import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, AgentThread
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.functions import KernelArguments

# Load environment variables from .env file
load_dotenv()

# Example questions (displayed at startup)
EXAMPLE_QUESTIONS = [
    "What's the weather forecast for Seattle? (latitude: 47.6062, longitude: -122.3321)",
    "Are there any weather alerts for Washington state?",
    "Can you get the forecast for New York City? (latitude: 40.7128, longitude: -74.0060)",
    "Get weather alerts for California (state code: CA)",
    "What's the forecast for Miami? (latitude: 25.7617, longitude: -80.1918)"
]


async def main():
    # Get configuration from environment variables
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    mcp_url = os.getenv("MCP_SERVER_URL")
    mcp_api_key = os.getenv("MCP_API_KEY")
    agent_name = os.getenv("AGENT_NAME", "WeatherAgent")
    agent_instructions = os.getenv("AGENT_INSTRUCTIONS", "You are a helpful weather assistant that can provide weather forecasts and alerts for any location.")

    # Validate required environment variables
    if not all([azure_endpoint, azure_api_key, deployment_name, mcp_url]):
        print("Error: Missing required environment variables. Please check your .env file.")
        print("Required: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME, MCP_SERVER_URL")
        return

    # Create Azure OpenAI service
    azure_openai_service = AzureChatCompletion(
        api_key=azure_api_key,
        endpoint=azure_endpoint,
        deployment_name=deployment_name
    )

    # Prepare headers for MCP connection if API key is provided
    mcp_headers = {}
    if mcp_api_key:
        mcp_headers["x-api-key"] = mcp_api_key

    # Validate MCP URL
    if not mcp_url:
        print("Error: MCP_SERVER_URL is required")
        return

    # Load the MCP Server as Plugin
    async with MCPSsePlugin(
        name="WeatherTools",
        url=mcp_url,
        headers=mcp_headers    ) as weather_plugin:
        
        # Create the agent
        agent = ChatCompletionAgent(
            service=azure_openai_service,
            name=agent_name,
            instructions=agent_instructions,
            plugins=[weather_plugin],
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )
        
        print(f"Agent '{agent.name}' created successfully using Azure OpenAI model: {deployment_name}")
        print(f"Connected to MCP server at: {mcp_url}")
        print(f"Available MCP tools: WeatherTools plugin (get_forecast, get_alerts)")
        print("-" * 60)
        
        # Show example questions
        print("🌤️  Welcome to the Weather Agent! Here are some example questions:")
        for i, example in enumerate(EXAMPLE_QUESTIONS, 1):
            print(f"   {i}. {example}")
        print("\n💡 Tip: You can ask about weather forecasts (need lat/long) or alerts (need US state code)")
        print("💡 Type 'goodbye' to exit the application")
        print("=" * 60)
        
        # Create a thread to hold the conversation
        thread: AgentThread | None = None
        question_count = 0
        
        while True:
            # Get user input
            try:
                user_input = input("\n🤔 Ask me about the weather: ").strip()
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Weather Agent!")
                break
            
            # Check for exit conditions
            if user_input.lower() in ['goodbye', 'bye', 'exit', 'quit']:
                print("\n👋 Goodbye! Thanks for using the Weather Agent!")
                break
            
            # Skip empty inputs
            if not user_input:
                print("❓ Please ask a weather question, or type 'goodbye' to exit.")
                continue
            
            question_count += 1
            print(f"\n# Question {question_count}: {user_input}", end="\n\n")
            first_chunk = True
            response_content = ""
            
            try:
                async for response in agent.invoke_stream(
                    messages=user_input,
                    thread=thread
                ):
                    if first_chunk:
                        print(f"# {response.name}: ", end="", flush=True)
                        first_chunk = False
                    print(response.content, end="", flush=True)
                    if response.content:
                        response_content += str(response.content)
                    thread = response.thread
                
                # Show MCP server interaction info
                print(f"\n\n🔌 MCP Server Information:")
                print(f"   - Connected to: WeatherTools MCP Server")
                print(f"   - Server URL: {mcp_url}")
                print(f"   - Available functions: get_forecast(), get_alerts()")
                print(f"   - Authentication: {'API Key' if mcp_api_key else 'None'}")
                
                # Show model and usage info
                print(f"\n📊 Model & Usage Information:")
                print(f"   - Model: {deployment_name} (Azure OpenAI)")
                print(f"   - Input length: {len(user_input.split())} words")
                print(f"   - Response length: {len(response_content.split())} words")
                print(f"   - Total questions asked: {question_count}")
                
                # Estimate token usage (rough approximation)
                estimated_input_tokens = int(len(user_input.split()) * 1.3)
                estimated_output_tokens = int(len(response_content.split()) * 1.3)
                print(f"   - Estimated input tokens: ~{estimated_input_tokens}")
                print(f"   - Estimated output tokens: ~{estimated_output_tokens}")
                
                print("\n" + "="*60)
                
            except Exception as e:
                print(f"\n❌ Error processing your question: {str(e)}")
                print("Please try again or type 'goodbye' to exit.")
                print("="*60)
        
        # Show final session summary
        print(f"\n📈 Final Session Summary:")
        print(f"   - Total questions processed: {question_count}")
        print(f"   - MCP Server: WeatherTools ({mcp_url})")
        print(f"   - Azure OpenAI Model: {deployment_name}")
        print(f"   - All weather data sourced from National Weather Service API")
        print("-" * 60)

        # Cleanup: Clear the thread
        if thread:
            await thread.delete()


if __name__ == "__main__":
    asyncio.run(main())