# Import pytest to handle assertions and fixtures
import pytest
# Import os to manipulate test environment variables
import os
# Import our new functions from app.py
from app import get_system_status, validate_config_key

def test_get_system_status_default():
    # Call status function without setting APP_ENV variable
    status = get_system_status()
    
    # Assert default environment falls back to 'development'
    assert status["environment"] == "development"
    # Assert operational status flag is present
    assert status["status"] == "OPERATIONAL"

def test_get_system_status_custom_env(monkeypatch):
    # Use pytest's built-in 'monkeypatch' fixture to temporarily inject an environment variable
    monkeypatch.setenv("APP_ENV", "production")
    
    # Execute status function
    status = get_system_status()
    
    # Verify function captured the patched environment variable
    assert status["environment"] == "production"

def test_validate_config_key_missing():
    # Assert that asking for a non-existent environment variable raises KeyError
    with pytest.raises(KeyError, match="Missing required environment variable"):
        validate_config_key("NON_EXISTENT_SECRET_KEY")

def test_validate_config_key_present(monkeypatch):
    # Temporarily set a mock API key in environment variables
    monkeypatch.setenv("MOCK_API_KEY", "secret_12345")
    
    # Assert function returns True when key exists
    assert validate_config_key("MOCK_API_KEY") is True