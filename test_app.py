# Import pytest to handle assertions and fixtures
import pytest
# Import os to manipulate test environment variables
import os
# Import pathlib Path to work with paths returned by tmp_path
from pathlib import Path
# Import all functions from app.py
from app import (
    calculate_average,
    format_user_role,
    save_user_record,
    read_user_record,
    get_system_status,
    validate_config_key
)

def test_calculate_average_valid():
    assert calculate_average([10, 20, 30]) == 20.0

def test_calculate_average_empty():
    with pytest.raises(ValueError, match="Cannot calculate the average"):
        calculate_average([])

def test_format_user_role_admin():
    assert format_user_role("admin") == "ACCESS_LEVEL_HIGH"

def test_save_and_read_user_record(tmp_path: Path):
    test_file = tmp_path / "user_101.json"
    payload = {"name": "Ade", "role": "Lead Tech"}
    
    assert save_user_record(str(test_file), 101, payload) is True
    assert test_file.exists()
    
    retrieved_data = read_user_record(str(test_file))
    assert retrieved_data["id"] == 101
    assert retrieved_data["name"] == "Ade"

def test_read_user_record_missing_file(tmp_path: Path):
    non_existent_file = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError, match="Record file not found"):
        read_user_record(str(non_existent_file))

def test_save_user_record_invalid_id(tmp_path: Path):
    test_file = tmp_path / "invalid_user.json"
    with pytest.raises(ValueError, match="User ID must be a positive integer"):
        save_user_record(str(test_file), -5, {"name": "Test"})

def test_get_system_status_default():
    status = get_system_status()
    assert status["environment"] == "development"
    assert status["status"] == "OPERATIONAL"

def test_get_system_status_custom_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    status = get_system_status()
    assert status["environment"] == "production"

def test_validate_config_key_missing():
    with pytest.raises(KeyError, match="Missing required environment variable"):
        validate_config_key("NON_EXISTENT_SECRET_KEY")

def test_validate_config_key_present(monkeypatch):
    monkeypatch.setenv("MOCK_API_KEY", "secret_12345")
    assert validate_config_key("MOCK_API_KEY") is True