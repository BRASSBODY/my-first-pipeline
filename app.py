import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Union


def calculate_average(numbers: List[Union[int, float]]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list.")

    return sum(numbers) / len(numbers)


def format_user_role(role: str) -> str:
    cleaned_role = role.strip().lower()

    if cleaned_role in ["admin", "lead"]:
        return "ACCESS_LEVEL_HIGH"
    elif cleaned_role in ["user", "guest"]:
        return "ACCESS_LEVEL_STANDARD"
    else:
        raise ValueError(f"Invalid role provided: {role}")


def save_user_record(file_path: str, user_id: int, user_data: Dict[str, Any]) -> bool:
    target_file = Path(file_path)

    if user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    user_data["id"] = user_id

    with open(target_file, mode="w", encoding="utf-8") as file_handle:
        json.dump(user_data, file_handle, indent=2)

    return True


def read_user_record(file_path: str) -> Dict[str, Any]:
    target_file = Path(file_path)

    if not target_file.exists():
        raise FileNotFoundError(f"Record file not found at: {file_path}")

    with open(target_file, mode="r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    return data


def get_system_status() -> Dict[str, Any]:
    env = os.getenv("APP_ENV", "development")
    current_time = datetime.now(timezone.utc).isoformat()

    return {"environment": env, "timestamp": current_time, "status": "OPERATIONAL"}


def validate_config_key(key_name: str) -> bool:
    value = os.getenv(key_name)

    if not value:
        raise KeyError(f"Missing required environment variable: {key_name}")

    return True


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
            "access_level": access_level,
        }

        self._users[user_id] = user_record
        return user_record

    def get_user(self, user_id: int) -> Dict[str, Any]:
        if user_id not in self._users:
            raise KeyError(f"User ID {user_id} not found.")

        return self._users[user_id]

    def get_total_users(self) -> int:
        return len(self._users)


def fetch_database_credentials() -> Dict[str, str]:
    """Retrieves sensitive database credentials injected by system environment."""
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")

    if not db_user or not db_pass:
        raise ValueError("Database credentials missing from environment.")

    return {"user": db_user, "password": db_pass, "connection_status": "READY"}
