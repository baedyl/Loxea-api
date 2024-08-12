import os
import sys
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

base_dir = os.path.abspath(sys.path[0])


class FactoryConfig(BaseSettings):
    SERVER_NAME: str
    SERVER_HOST: str
    SERVER_PORT: str
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60  # 1 day expressed in minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 5 * 24 * 60  # 5 days expressed in minutes
    ENVIRONMENT: Literal["dev", "prod"]
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None
    GCP_AUTH_SERVICE_FILE: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def settings():
    return FactoryConfig()


config = settings()
