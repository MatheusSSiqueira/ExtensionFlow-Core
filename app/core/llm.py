"""Utilitários para trabalhar com o modelo Gemini (Google Generative AI).

Este módulo fornece uma função simples para retornar uma instância
pré-configurada do modelo Gemini usada pela aplicação.
"""

import google.generativeai as genai
from app.core.config import settings

# Inicializa o SDK do Google com a chave da configuração (variável de ambiente).
genai.configure(api_key=settings.gemini_api_key)

def get_gemini_model(model_name: str = "gemini-3.6-flash", temperature: float = 0.0):
    """Retorna uma instância configurada do modelo Gemini.

    Args:
        model_name: Nome do modelo Gemini a ser usado.
        temperature: Controle de aleatoriedade na geração (0.0 = determinístico).

    Returns:
        Uma instância de `genai.GenerativeModel` pronta para gerar conteúdo.
    """

    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=genai.GenerationConfig(
            temperature=temperature
        )
    )