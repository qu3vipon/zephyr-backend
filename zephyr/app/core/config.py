import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"

    # Environment Variables
    DB_NAME: str = os.getenv("DB_NAME", "zephyr_dev")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "zephyr")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost:5432")
    DB_USER: str = os.getenv("DB_USER", "zephyr")
    ENVIRONMENT: str = os.getenv("ENV", "dev")
    SECRET_KEY: str = os.getenv("SECREY_KEY", "zephyr")
    TESTING: bool = os.getenv("TESTING", 0)

    @property
    def _database_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()