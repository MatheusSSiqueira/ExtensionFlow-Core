import google.generativeai as genai
from app.core.llm import get_gemini_model
from app.schemas.compliance import ComplianceChecklist

def analyze_compliance_with_gemini(activity_description: str, regulation_context: str) -> dict:
    """
    Envia a atividade para o Gemini e obriga a resposta a seguir o Schema Pydantic.
    """
    model = get_gemini_model()
    
    prompt = f"""
    Você é um validador de atividades acadêmicas. Use APENAS o regulamento abaixo para avaliar a atividade.
    Não invente regras.
    
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
    
    import json
    return json.loads(response.text)