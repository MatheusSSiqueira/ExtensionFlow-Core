import google.generativeai as genai
from app.core.config import settings

# Configura o SDK do Google com a chave segura
genai.configure(api_key=settings.gemini_api_key)

def get_gemini_model(model_name: str = "gemini-2.5-flash", temperature: float = 0.0):
    
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=genai.GenerationConfig(
            temperature=temperature
        )
    )