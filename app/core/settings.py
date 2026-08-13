from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    SERVICE_NAME: str = Field(env="SERVICE_NAME")
    DATABASE_NAME: str = Field(env="DATABASE_NAME")


config = Config()
