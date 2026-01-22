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
    login_url: str = f"{base_url}"
    self_service_url: str = f"{base_url}personal/self-service"
    edit_self_service_url: str = f"{base_url}personal/self-service/personal-data/edit"
    add_bank_details_url: str = f"{base_url}personal/self-service/bank-details/add"


    # Test Credentials
    test_username: str = ""
    test_password: str = ""
    test_wrong_username: str = "bonduu001@yahoo.com"
    test_wrong_password: str = "Bat165474@@"
    test_other_name: str = "OLADEJO"
    test_job_title: str = "HEAD OF IT"
    bank_name: str = "GLOBUS BANK"
    bank_id: str = "UNAFNGLA228"
    sort_code: str = "033"
    first_name: str = ""
    other_name: str = ""
    surname: str = ""
    maiden_name: str = ""
    previous_name: str = ""
    mobile_number: str = ""
    work_number: str = ""
    relationship: str = ""
    email: str = ""
    location: str = ""
    relationship_1: str = ""
    test_bvn_number: str = '22857690876'

    # Browser Settings
    headless: bool = False
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
