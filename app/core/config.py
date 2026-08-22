from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "ExtensionFlow"
    gemini_api_key: str
    
    # Isso diz ao Pydantic para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()