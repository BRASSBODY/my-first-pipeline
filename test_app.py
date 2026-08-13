# Import pytest to handle test assertions and fixture dependencies
import pytest
# Import pathlib Path to work with paths returned by tmp_path
from pathlib import Path
# Import functions to test from app.py
from app import calculate_average, format_user_role, save_user_record, read_user_record

def test_calculate_average_valid():
    # Verify calculation of positive numbers
    assert calculate_average([10, 20, 30]) == 20.0

def test_calculate_average_empty():
    # Verify exception on empty dataset
    with pytest.raises(ValueError, match="Cannot calculate the average"):
        calculate_average([])

def test_format_user_role_admin():
    # Verify role formatting for high access levels
    assert format_user_role("admin") == "ACCESS_LEVEL_HIGH"

def test_save_and_read_user_record(tmp_path: Path):
    # Pass pytest's 'tmp_path' fixture as an argument; pytest injects a temporary directory Path object
    test_file = tmp_path / "user_101.json"
    
    # Define payload dictionary to save
    payload = {"name": "Ade", "role": "Lead Tech"}
    
    # Execute save operation targeting temporary path
    save_result = save_user_record(str(test_file), 101, payload)
    
    # Verify that the function returned True indicating success
    assert save_result is True
    # Verify that the physical file was actually created on disk inside the temp folder
    assert test_file.exists()
    
    # Read the data back using our read function
    retrieved_data = read_user_record(str(test_file))
    
    # Assert that saved data matches original payload including assigned ID
    assert retrieved_data["id"] == 101
    assert retrieved_data["name"] == "Ade"

def test_read_user_record_missing_file(tmp_path: Path):
    # Construct a path to a non-existent file in the temp folder
    non_existent_file = tmp_path / "missing.json"
    
    # Assert that trying to read a non-existent file raises FileNotFoundError
    with pytest.raises(FileNotFoundError, match="Record file not found"):
        read_user_record(str(non_existent_file))

def test_save_user_record_invalid_id(tmp_path: Path):
    # Path to temp file
    test_file = tmp_path / "invalid_user.json"
    
    # Verify that passing a negative ID raises a ValueError
    with pytest.raises(ValueError, match="User ID must be a positive integer"):
        save_user_record(str(test_file), -5, {"name": "Test"})