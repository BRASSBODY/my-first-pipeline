# Import pytest so we can test expected exceptions
import pytest
# Import the functions we want to test from app.py
from app import calculate_average, format_user_role

def test_calculate_average_valid():
    # Define a sample list of integers
    nums = [10, 20, 30]
    # Assert that the average of 10, 20, and 30 is exactly 20.0
    assert calculate_average(nums) == 20.0

def test_calculate_average_empty():
    # Verify that passing an empty list raises a ValueError exception
    with pytest.raises(ValueError, match="Cannot calculate the average"):
        calculate_average([])

def test_format_user_role_admin():
    # Verify that 'admin' returns high access status
    assert format_user_role("admin") == "ACCESS_LEVEL_HIGH"
    # Verify that extra whitespace and mixed casing are handled correctly
    assert format_user_role("  LEAD  ") == "ACCESS_LEVEL_HIGH"

def test_format_user_role_invalid():
    # Verify that an invalid role string raises a ValueError
    with pytest.raises(ValueError, match="Invalid role provided"):
        format_user_role("unknown_role")