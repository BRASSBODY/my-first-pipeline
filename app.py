# Import the typing module to add type hints for better code readability
from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    # Check if the input list is empty to prevent a ZeroDivisionError
    if not numbers:
        # Raise a ValueError with a helpful message if the list contains no items
        raise ValueError("Cannot calculate the average of an empty list.")
    
    # Calculate the sum of all elements in the list and divide by the total count
    total_sum = sum(numbers)
    # Store the total number of elements in the list
    count = len(numbers)
    
    # Return the calculated average value
    return total_sum / count

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

# Standard main block ensuring code only runs when executing this file directly
if __name__ == "__main__":
    # Define a test dataset of numbers
    data = [10, 20, 30, 40]
    # Print the average of the dataset
    print(f"Average: {calculate_average(data)}")