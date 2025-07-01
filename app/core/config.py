from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_URI: str = "postgresql://postgres:postgres@localhost:5432/sample"

    class Config:
        env_file = "../.env"


settings = Settings()