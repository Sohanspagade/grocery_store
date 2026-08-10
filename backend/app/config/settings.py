from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_database: str = "smartcart"
    openrouter_api_key: str
    openrouter_model: str = "openai/gpt-3.5-turbo"
    port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
