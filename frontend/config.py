from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignoriert unbekannte Felder

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings