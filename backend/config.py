from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings configuration class for the URL shortener backend.

    Attributes:
        env_name (str): The name of the environment (e.g., "Local", "Production").
        base_url (str): The base URL for the application.
        db_url (str): The database connection URL.
    """

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        """Configuration class for the application."""

        env_file: str = ".env"


def get_settings() -> Settings:
    """Get the application settings.

    Returns:
        Settings (Settings): The application settings.
    """
    settings: Settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
