import google.generativeai as genai
from app.core.config import settings

# Autentica com a sua chave
genai.configure(api_key=settings.gemini_api_key)

print("Buscando modelos de Embedding disponíveis...")

# Pede ao Google a lista de todos os modelos
for m in genai.list_models():
    # Filtra apenas os modelos que suportam a criação de vetores (embedContent)
    if 'embedContent' in m.supported_generation_methods:
        print(f"✅ Modelo Encontrado: {m.name}")