from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "ExtensionFlow"
    gemini_api_key: str
    
    # Instrui o Pydantic a carregar variáveis a partir do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()