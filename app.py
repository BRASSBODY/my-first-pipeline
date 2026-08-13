# Import os to read environment variables set by the system or CI runner
import os
# Import datetime to format timestamps
from datetime import datetime
# Import typing helpers for explicit type annotations
from typing import Dict, Any

def get_system_status() -> Dict[str, Any]:
    # Read the current deployment environment from system environment variables (default to 'development')
    env = os.getenv("APP_ENV", "development")
    
    # Generate an ISO-formatted timestamp representing current UTC time
    current_time = datetime.utcnow().isoformat()
    
    # Return a structured dictionary containing environment metadata
    return {
        "environment": env,
        "timestamp": current_time,
        "status": "OPERATIONAL"
    }

def validate_config_key(key_name: str) -> bool:
    # Fetch the environment variable value associated with key_name
    value = os.getenv(key_name)
    
    # If the key is missing or empty, raise a KeyError to enforce required settings
    if not value:
        raise KeyError(f"Missing required environment variable: {key_name}")
        
    # Return True if key exists and contains a non-empty string
    return True