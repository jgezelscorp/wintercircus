"""
API Key Authentication Module

This module implements API key-based authentication for the FastAPI application.
It validates incoming requests against a list of approved API keys stored in
the API_KEYS environment variable.

The authentication is implemented as a FastAPI dependency that can be injected
into route handlers or applied globally to the application.

Features:
- Validates API keys from the x-api-key header
- Retrieves valid keys from environment variables
- Rejects requests with invalid keys with a 403 Forbidden response

Usage:
    from api_key_auth import ensure_valid_api_key
    
    # Apply to a specific endpoint
    @app.get("/protected", dependencies=[Depends(ensure_valid_api_key)])
    def protected_route():
        return {"message": "Access granted"}
        
    # Or apply globally to all routes
    app = FastAPI(dependencies=[Depends(ensure_valid_api_key)])
"""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

# Define the API key header schema for FastAPI's security system
# This specifies that we expect API keys in the "x-api-key" header
api_key_header = APIKeyHeader(name="x-api-key")

def ensure_valid_api_key(api_key_header: str = Security(api_key_header)):
    """
    FastAPI dependency that validates the API key provided in the request header.
    
    This function is designed to be used as a dependency in FastAPI routes.
    It extracts the API key from the x-api-key header and validates it against
    a list of approved keys stored in the API_KEYS environment variable.
    
    Args:
        api_key_header (str): The API key extracted from the request header.
                              This is injected automatically by FastAPI's Security system.
    
    Returns:
        None: If the API key is valid, the function returns normally and request processing continues.
        
    Raises:
        HTTPException: If the API key is invalid or missing, raises a 403 Forbidden exception,
                      which will return an error response to the client.
    
    Environment Variables:
        API_KEYS: Comma-separated list of valid API keys.
    """
    def check_api_key(key: str) -> bool:
        """
        Helper function to check if an API key is valid.
        
        Args:
            key (str): The API key to validate
            
        Returns:
            bool: True if the key is valid, False otherwise
        """
        # Get list of valid keys from environment variables
        # If the environment variable isn't set, default to an empty string
        valid_keys = os.environ.get("API_KEYS", "").split(",")
        
        # A key is valid if it's in the list of valid keys and not empty
        return key in valid_keys and key != ""

    # Check if the provided API key is valid
    if not check_api_key(api_key_header):
        # If invalid, raise an HTTP exception with 403 Forbidden status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
