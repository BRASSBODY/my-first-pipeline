# Import json module to handle reading and writing JSON data files
import json
# Import os to read environment variables set by the system or CI runner
import os
# Import datetime to format timestamps
from datetime import datetime
# Import Path class from pathlib to work with file paths safely across operating systems
from pathlib import Path
# Import typing helpers to define function parameter and return types
from typing import Dict, Any, List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    # Check if the input list is empty to prevent a ZeroDivisionError
    if not numbers:
        # Raise a ValueError with a helpful message if the list contains no items
        raise ValueError("Cannot calculate the average of an empty list.")
    
    # Calculate total sum divided by length
    return sum(numbers) / len(numbers)

def format_user_role(role: str) -> str:
    # Strip leading/trailing whitespace and convert string to lower case
    cleaned_role = role.strip().lower()
    
    # Check if role matches allowed administrative roles
    if cleaned_role in ["admin", "lead"]:
        return "ACCESS_LEVEL_HIGH"
    elif cleaned_role in ["user", "guest"]:
        return "ACCESS_LEVEL_STANDARD"
    else:
        raise ValueError(f"Invalid role provided: {role}")

def save_user_record(file_path: str, user_id: int, user_data: Dict[str, Any]) -> bool:
    # Convert string file path into a Path object
    target_file = Path(file_path)
    
    # Verify user_id is positive
    if user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    
    user_data["id"] = user_id
    
    # Write JSON data to disk
    with open(target_file, mode="w", encoding="utf-8") as file_handle:
        json.dump(user_data, file_handle, indent=2)
        
    return True

def read_user_record(file_path: str) -> Dict[str, Any]:
    # Convert string file path into a Path object
    target_file = Path(file_path)
    
    if not target_file.exists():
        raise FileNotFoundError(f"Record file not found at: {file_path}")
        
    # Read JSON data from disk
    with open(target_file, mode="r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)
        
    return data

def get_system_status() -> Dict[str, Any]:
    # Read environment variable with default fallback
    env = os.getenv("APP_ENV", "development")
    current_time = datetime.utcnow().isoformat()
    
    return {
        "environment": env,
        "timestamp": current_time,
        "status": "OPERATIONAL"
    }

def validate_config_key(key_name: str) -> bool:
    # Check if essential env variable is defined
    value = os.getenv(key_name)
    
    if not value:
        raise KeyError(f"Missing required environment variable: {key_name}")
        
    return True