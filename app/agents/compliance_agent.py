import google.generativeai as genai
from app.core.llm import get_gemini_model
from app.schemas.compliance import ComplianceChecklist
import json

def analyze_compliance_with_gemini(activity_description: str, regulation_context: str) -> dict:
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
    
    return json.loads(response.text)