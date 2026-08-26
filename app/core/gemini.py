from google import genai
from google.genai import types
from app.core.config import settings

# Inicializa o cliente centralizado do SDK oficial
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_gemini_client() -> genai.Client:
    """Retorna a instância única do cliente Gemini."""
    return client

def get_default_config(response_schema=None) -> types.GenerateContentConfig:
    """
    Retorna a configuração padrão do MVP.
    Força a temperatura baixa e, se um schema Pydantic for passado,
    configura o Structured Output nativamente.
    """
    config_args = {
        "temperature": settings.GEMINI_TEMPERATURE,
    }
    
    if response_schema:
        config_args["response_mime_type"] = "application/json"
        config_args["response_schema"] = response_schema
        
    return types.GenerateContentConfig(**config_args)