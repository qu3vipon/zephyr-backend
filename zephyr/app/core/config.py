import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(APP_DIR)
ROOT_DIR = os.path.dirname(PROJECT_DIR)


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_V1_PREFIX: str = "/api/v1"

    # Environment Variables
    DB_NAME: str = os.getenv("DB_NAME", "zephyr_dev")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "zephyr")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")

    @property
    def DB_URL(self):  # noqa
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"

    DB_USER: str = os.getenv("DB_USER", "zephyr")
    ENVIRONMENT: str = os.getenv("ENV", "dev")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "zephyr")
    SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "zephyr")
    SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "zephyr")
    TESTING: bool = os.getenv("TESTING", 0)
    TEST_USERNAME = "zephyr"
    TEST_PASSWORD = "zephyr"


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()
