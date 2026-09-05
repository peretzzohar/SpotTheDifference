from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_title: str = "-SpotTheDifference Skeleton API"
    api_version: str = "0.1.0"
    cors_origins: str = "http://localhost:5172,http://127.0.0.1:5172"
    model_path: Path | None = None
    inference_api_url: str = "http://localhost:8009/api/v1/analyze"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

settings = Settings()
