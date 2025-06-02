import React from 'react';
import { useMsal } from '@azure/msal-react';
import { loginRequest } from '../authConfig';

const LoginButton = () => {
  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginPopup(loginRequest).catch(e => {
      console.error('Login failed:', e);
    });
  };

  return (
    <div className="login-container">
      <h1>🌤️ Weather Agent</h1>
      <p>
        Welcome to your AI-powered weather assistant! 
        Please sign in with your Microsoft account to access the weather services.
      </p>
      <button className="login-button" onClick={handleLogin}>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M7.462 0H0v7.462h7.462V0zM16 0H8.538v7.462H16V0zM7.462 8.538H0V16h7.462V8.538zM16 8.538H8.538V16H16V8.538z"/>
        </svg>
        Sign in with Microsoft
      </button>
    </div>
  );
};

export default LoginButton;
