import React from 'react';
import { AuthenticatedTemplate, UnauthenticatedTemplate, useIsAuthenticated, useMsal } from '@azure/msal-react';
import LoginButton from './components/LoginButton';
import WeatherChat from './components/WeatherChat';

function App() {
  const isAuthenticated = useIsAuthenticated();
  const { accounts } = useMsal();
  
  const user = accounts[0] ? {
    name: accounts[0].name,
    username: accounts[0].username
  } : null;

  return (
    <div className="app">
      <UnauthenticatedTemplate>
        <LoginButton />
      </UnauthenticatedTemplate>
      
      <AuthenticatedTemplate>
        <WeatherChat user={user} />
      </AuthenticatedTemplate>
    </div>
  );
}

export default App;
