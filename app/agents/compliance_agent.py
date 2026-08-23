"""Agente de conformidade que utiliza o modelo Gemini para avaliar atividades.

Esta função consulta o LLM com um prompt estruturado e pede uma resposta
no formato do `ComplianceChecklist`. A função devolve um dicionário
que pode ser usado para construir o modelo Pydantic correspondente.
"""

import google.generativeai as genai
from app.core.llm import get_gemini_model
from app.schemas.compliance import ComplianceChecklist
import json


def analyze_compliance_with_gemini(activity_description: str, regulation_context: str) -> dict:
    """Avalia a conformidade de uma atividade com base em um regulamento.

    Args:
        activity_description: Texto descritivo da atividade do aluno.
        regulation_context: Trechos relevantes do regulamento (contexto RAG).

    Returns:
        Um dicionário compatível com o schema `ComplianceChecklist`.
    """

    # Instancia o modelo Gemini (camada de abstração em app.core.llm)
    model = get_gemini_model()

    prompt = f"""
    Você é um auditor rigoroso de atividades acadêmicas. Sua função é avaliar a atividade do aluno com base ÚNICA e EXCLUSIVAMENTE no regulamento fornecido.
    
    Regras de análise:
    1. Leia a atividade do aluno.
    2. Identifique no regulamento qual artigo ou regra se aplica a ela.
    3. Ignore os artigos que não têm relação com a atividade descrita.
    4. Cuidado com a palavra "OU". Se a regra diz "A ou B", fornecer apenas um dos dois é suficiente.
    
    REGULAMENTO:
    {regulation_context}
    
    ATIVIDADE DO ALUNO:
    {activity_description}
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=ComplianceChecklist, 
        ),
    )

    # O SDK retorna um texto JSON; convertendo para dicionário Python
    return json.loads(response.text)