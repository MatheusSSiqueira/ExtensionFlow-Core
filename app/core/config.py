from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "ExtensionFlow API"
    ENVIRONMENT: str = "development"
    CORS_ALLOWED_ORIGINS: str = "*"

    # Configurações do Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        """Converte a string do .env em uma lista para o FastAPI"""
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]

settings = Settings()