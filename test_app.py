# Standard library imports
import os
from pathlib import Path

# Third-party testing framework
import pytest

# Local application imports
from app import (
    calculate_average,
    format_user_role,
    save_user_record,
    read_user_record,
    get_system_status,
    validate_config_key,
    UserManager,
    fetch_database_credentials,
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


def test_get_system_status_default(monkeypatch):
    # Safely remove APP_ENV if set by CI runner to test default fallback behavior
    monkeypatch.delenv("APP_ENV", raising=False)

    # Execute status call
    status = get_system_status()

    # Now it cleanly falls back to 'development'
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


# --- UserManager Tests ---


@pytest.fixture
def manager() -> UserManager:
    return UserManager("ProductionSystem")


def test_user_manager_add_and_get(manager: UserManager):
    user = manager.add_user(1, "Ade", "admin")
    assert user["id"] == 1
    assert user["access_level"] == "ACCESS_LEVEL_HIGH"

    retrieved = manager.get_user(1)
    assert retrieved["name"] == "Ade"
    assert manager.get_total_users() == 1


def test_user_manager_duplicate_id(manager: UserManager):
    manager.add_user(1, "Ade", "admin")
    with pytest.raises(KeyError, match="already exists"):
        manager.add_user(1, "Bisi", "user")


def test_user_manager_get_missing_user(manager: UserManager):
    with pytest.raises(KeyError, match="not found"):
        manager.get_user(999)


# --- Database Credentials Tests ---


def test_fetch_database_credentials_missing():
    with pytest.raises(ValueError, match="Database credentials missing"):
        fetch_database_credentials()


def test_fetch_database_credentials_success(monkeypatch):
    monkeypatch.setenv("DB_USER", "admin_user")
    monkeypatch.setenv("DB_PASSWORD", "super_secret_123")

    creds = fetch_database_credentials()
    assert creds["user"] == "admin_user"
    assert creds["password"] == "super_secret_123"
    assert creds["connection_status"] == "READY"


def test_format_user_role_standard():
    # Covers fallback role logic
    assert format_user_role("user") == "ACCESS_LEVEL_STANDARD"


def test_user_manager_invalid_id(manager: UserManager):
    with pytest.raises(ValueError, match="User ID must be a positive integer"):
        manager.add_user(-1, "Test", "user")


def test_fetch_database_credentials_missing(monkeypatch):
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="Database credentials missing"):
        fetch_database_credentials()
