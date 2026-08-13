# Import json module to handle reading and writing JSON data files
import json
# Import Path class from pathlib to work with file paths safely across operating systems
from pathlib import Path
# Import typing helpers to define function parameter and return types
from typing import Dict, Any, List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    # Check if the input list is empty to prevent a ZeroDivisionError
    if not numbers:
        # Raise a ValueError with a helpful message if the list contains no items
        raise ValueError("Cannot calculate the average of an empty list.")
    
    # Calculate the sum of all elements in the list and divide by the total count
    return sum(numbers) / len(numbers)

def format_user_role(role: str) -> str:
    # Strip leading/trailing whitespace and convert the string to lower case
    cleaned_role = role.strip().lower()
    
    # Check if the role matches allowed administrative roles
    if cleaned_role in ["admin", "lead"]:
        # Return capitalized elevated access level
        return "ACCESS_LEVEL_HIGH"
    # Check if the role matches standard user roles
    elif cleaned_role in ["user", "guest"]:
        # Return capitalized basic access level
        return "ACCESS_LEVEL_STANDARD"
    else:
        # Handle unknown roles by raising an exception
        raise ValueError(f"Invalid role provided: {role}")

def save_user_record(file_path: str, user_id: int, user_data: Dict[str, Any]) -> bool:
    # Convert string file path into a Path object for OS-agnostic operations
    target_file = Path(file_path)
    
    # Check if the user ID is a positive integer
    if user_id <= 0:
        # Raise an exception if an invalid user ID is provided
        raise ValueError("User ID must be a positive integer.")
    
    # Add the user_id directly into the payload dictionary
    user_data["id"] = user_id
    
    # Open target file path in write mode ('w') with UTF-8 character encoding
    with open(target_file, mode="w", encoding="utf-8") as file_handle:
        # Serialize python dictionary into JSON format and write to disk with formatting
        json.dump(user_data, file_handle, indent=2)
        
    # Return True indicating successful save operation
    return True

def read_user_record(file_path: str) -> Dict[str, Any]:
    # Convert string file path into a Path object
    target_file = Path(file_path)
    
    # Check if the specified file actually exists on the filesystem
    if not target_file.exists():
        # Raise a FileNotFoundError if the path points to a non-existent file
        raise FileNotFoundError(f"Record file not found at: {file_path}")
        
    # Open target file path in read mode ('r') with UTF-8 character encoding
    with open(target_file, mode="r", encoding="utf-8") as file_handle:
        # Parse JSON data from file directly into a Python dictionary
        data = json.load(file_handle)
        
    # Return the dictionary containing user data
    return data