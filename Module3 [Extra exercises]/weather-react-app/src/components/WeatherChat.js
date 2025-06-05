import React, { useState, useRef, useEffect } from 'react';
import { useMsal } from '@azure/msal-react';
import { apiConfig } from '../authConfig';

const WeatherChat = ({ user }) => {
  const { instance } = useMsal();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [questionCount, setQuestionCount] = useState(0);
  const messagesEndRef = useRef(null);  const exampleQuestions = [
    "What's the weather forecast for Seattle?",
    "Get weather alerts for Washington",
    "Show me the forecast for New York City", 
    "Get weather alerts for California",
    "What's the weather like in Miami?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleLogout = () => {
    instance.logoutPopup().catch(e => {
      console.error('Logout failed:', e);
    });
  };  const callWeatherAgent = async (question) => {
    try {
      console.log('Calling MCP server at:', apiConfig.mcpServer.url);
      console.log('With API key:', apiConfig.mcpServer.apiKey ? 'Present' : 'Missing');
      
      // For now, let's test direct connection to your MCP server
      // Since your MCP server is exposed via SSE, we'll try a direct approach
      
      // Parse the question to extract function calls
      const lowerQuestion = question.toLowerCase();
      let mcpResponse;
        if (lowerQuestion.includes('forecast') || lowerQuestion.includes('weather for') || lowerQuestion.includes('weather like')) {
        // Extract location from natural language
        const locationMatch = question.match(/(?:for|in|at)\s+([a-zA-Z\s,]+)/i);
        if (locationMatch) {
          const location = locationMatch[1].trim();
          mcpResponse = await callMCPFunction('get_forecast', { location });
        } else {
          return "To get a weather forecast, please specify a location like: 'What's the weather forecast for Seattle?' or 'Show me the forecast for New York City'";
        }
      } else if (lowerQuestion.includes('alert')) {
        // Extract location/state from natural language
        const locationMatch = question.match(/(?:for|in|at)\s+([a-zA-Z\s,]+)/i);
        if (locationMatch) {
          const location = locationMatch[1].trim();
          mcpResponse = await callMCPFunction('get_alerts', { location });
        } else {
          return "To get weather alerts, please specify a location like: 'Get weather alerts for Washington' or 'Show alerts for California'";
        }
      } else {
        return `I can help you with weather forecasts and alerts! Try asking:
• "What's the weather forecast for Seattle?"
• "Get weather alerts for Washington"
• "Show me the forecast for New York City"`;
      }
      
      // Format the MCP response nicely
      if (mcpResponse && mcpResponse.content) {
        return mcpResponse.content;
      } else if (mcpResponse) {
        return JSON.stringify(mcpResponse, null, 2);
      } else {
        return "No data received from weather service.";
      }
      
    } catch (error) {
      console.error('Weather API Error:', error);
      throw new Error(`Failed to get weather information: ${error.message}`);
    }
  };
  const callMCPFunction = async (functionName, args) => {
    try {
      console.log(`Calling MCP function: ${functionName}`, args);
      
      // Your MCP server uses SSE protocol which is complex for browser calls
      // Let's try a direct test first to see if CORS is enabled
      const testUrl = apiConfig.mcpServer.url.replace('/sse', '/test');
      
      const response = await fetch(apiConfig.mcpServer.url, {
        method: 'GET',
        headers: {
          'x-api-key': apiConfig.mcpServer.apiKey,
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache',
        },
        mode: 'cors' // Enable CORS
      });

      if (!response.ok) {
        throw new Error(`MCP server connection failed: ${response.status} ${response.statusText}`);
      }

      // For now, return a message about the connection
      return {
        content: `Successfully connected to MCP server at ${apiConfig.mcpServer.url}. 
        Function requested: ${functionName} with args: ${JSON.stringify(args)}
        
        Note: Full MCP protocol implementation requires server-side proxy due to SSE complexity.
        Current status: Connection test ${response.ok ? 'successful' : 'failed'}`
      };
      
    } catch (error) {
      console.error('MCP Server Error:', error);
      
      // Check if it's a CORS error
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return {
          content: `⚠️ CORS Error: Cannot directly connect to MCP server from browser.
          
The MCP server at ${apiConfig.mcpServer.url} needs CORS headers to allow browser connections.

Suggested solutions:
1. Add CORS middleware to your MCP server
2. Create a backend proxy service
3. Use the weather data through Azure OpenAI (recommended approach)

Error details: ${error.message}`
        };
      }
      
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError('');
    setIsLoading(true);

    // Add user message
    const newUserMessage = {
      id: Date.now(),
      type: 'user',
      content: userMessage,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setQuestionCount(prev => prev + 1);    try {
      // Call Azure OpenAI with MCP server integration
      const response = await callWeatherAgent(userMessage);
      
      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response,
        timestamp: new Date(),
        metadata: {
          mcpServer: 'WeatherTools MCP Server',
          serverUrl: apiConfig.mcpServer.url,
          model: `${apiConfig.agent.name} (${apiConfig.azureOpenAI.deploymentName})`,
          inputWords: userMessage.split(' ').length,
          responseWords: response.split(' ').length
        }
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (err) {
      setError('Failed to get weather information. Please try again.');
      console.error('Weather API error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleExampleClick = (question) => {
    setInputValue(question);
  };

  return (
    <div className="weather-app">
      <div className="app-header">
        <h1>🌤️ Weather Agent</h1>
        <div className="user-info">
          <span>Welcome, {user?.name || 'User'}!</span>
          <button className="logout-button" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      </div>
      
      <div className="chat-container">
        <div className="messages-area">
          {messages.length === 0 && (
            <div className="example-questions">
              <h3>🌟 Example Questions:</h3>
              <ul>
                {exampleQuestions.map((question, index) => (
                  <li key={index} onClick={() => handleExampleClick(question)}>
                    {question}
                  </li>
                ))}
              </ul>
              <p><strong>💡 Tip:</strong> Click on any example above or type your own weather question!</p>
            </div>
          )}
          
          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}
          
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-label">
                {message.type === 'user' ? '🤔 You asked:' : '🤖 Weather Agent:'}
              </div>
              <div className="message-content">
                {message.content}
              </div>
              {message.metadata && (
                <div className="info-panel">
                  <h4>📊 Response Details:</h4>
                  <p><strong>MCP Server:</strong> {message.metadata.mcpServer}</p>
                  <p><strong>Model:</strong> {message.metadata.model}</p>
                  <p><strong>Input:</strong> {message.metadata.inputWords} words</p>
                  <p><strong>Response:</strong> {message.metadata.responseWords} words</p>
                  <p><strong>Question #{questionCount}</strong></p>
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="message assistant">
              <div className="message-label">🤖 Weather Agent:</div>
              <div className="loading">Getting weather information...</div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <div className="input-area">
          <div className="input-container">
            <textarea
              className="message-input"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about the weather... (e.g., What's the forecast for London?)"
              rows={1}
              disabled={isLoading}
            />
            <button
              className="send-button"
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
            >
              {isLoading ? '⏳' : '🚀'} Send
            </button>
          </div>
          <div style={{ marginTop: '10px', fontSize: '0.9rem', color: '#666' }}>
            💡 Connected to: {apiConfig.mcpServer.url} | Questions asked: {questionCount}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeatherChat;
