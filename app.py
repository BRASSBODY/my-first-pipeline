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

    class UserManager:
        """Manages user profiles and access roles in memory."""

    def __init__(self, system_name: str) -> None:
        # Store the system name as an instance attribute
        self.system_name = system_name
        # Private-like attribute storing user records (dictionary mapping user_id to user details)
        self._users: Dict[int, Dict[str, Any]] = {}

    def add_user(self, user_id: int, name: str, role: str) -> Dict[str, Any]:
        # Validate that the user ID is a positive integer
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        # Check if the user ID already exists in our dictionary
        if user_id in self._users:
            raise KeyError(f"User ID {user_id} already exists in {self.system_name}.")

        # Format and validate the role using our existing format_user_role function
        access_level = format_user_role(role)

        # Construct the user profile record
        user_record = {
            "id": user_id,
            "name": name,
            "role": role,
            "access_level": access_level
        }

        # Store the record in our internal dictionary
        self._users[user_id] = user_record

        # Return the created user record
        return user_record

    def get_user(self, user_id: int) -> Dict[str, Any]:
        # Check if the user exists; if not, raise a KeyError
        if user_id not in self._users:
            raise KeyError(f"User ID {user_id} not found.")

        # Return the requested user record dictionary
        return self._users[user_id]

    def get_total_users(self) -> int:
        # Return total count of users currently stored
        return len(self._users)


    class UserManager:
    """Manages user profiles and access roles in memory."""

    def __init__(self, system_name: str) -> None:
        self.system_name = system_name
        self._users: Dict[int, Dict[str, Any]] = {}

    def add_user(self, user_id: int, name: str, role: str) -> Dict[str, Any]:
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        if user_id in self._users:
            raise KeyError(f"User ID {user_id} already exists in {self.system_name}.")

        access_level = format_user_role(role)

        user_record = {
            "id": user_id,
            "name": name,
            "role": role,
            "access_level": access_level
        }

        self._users[user_id] = user_record
        return user_record

    def get_user(self, user_id: int) -> Dict[str, Any]:
        if user_id not in self._users:
            raise KeyError(f"User ID {user_id} not found.")

        return self._users[user_id]

    def get_total_users(self) -> int:
        return len(self._users)