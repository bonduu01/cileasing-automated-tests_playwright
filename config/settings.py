"""
Application settings loaded from environment variables.
Uses pydantic-settings for type-safe configuration management.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with automatic .env file loading."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application URLs
    base_url: str = "https://candileasing.netlify.app/"
    login_url: str = "https://candileasing.netlify.app/"
    self_service_url: str = "https://candileasing.netlify.app/personal/self-service"
    edit_self_service_url: str = "https://candileasing.netlify.app/personal/self-service/personal-data/edit"


    # Test Credentials
    test_username: str = ""
    test_password: str = ""
    test_wrong_username: str = "bonduu001@yahoo.com"
    test_wrong_password: str = "Bat165474@@"
    test_other_name: str = "OLADEJO"
    test_job_title: str = "HEAD OF IT"


    # Browser Settings
    headless: bool = True
    slow_mo: int = 0
    timeout: int = 30000

    # Video Recording
    record_video: bool = False
    video_dir: str = "videos/"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache for singleton-like behavior.
    """
    return Settings()


# Convenience export
settings = get_settings()
