from fastapi import APIRouter
from app.schemas.compliance import ComplianceRequest, ComplianceChecklist
from app.agents.compliance_agent import analyze_compliance_with_gemini

router = APIRouter()

MOCK_REGULATION = """
O aluno só pode realizar palestras se a carga horária for de no mínimo 4 horas.
É obrigatório apresentar um certificado de participação assinado pela instituição anfitriã.
"""

@router.post("/validate", response_model=ComplianceChecklist)
def validate_activity_endpoint(request: ComplianceRequest):
    """
    Recebe a intenção de atividade do usuário e retorna a validação estruturada.
    """
    # Chama o agente de IA passando a atividade e o contexto
    result_dict = analyze_compliance_with_gemini(
        activity_description=request.activity_description,
        regulation_context=MOCK_REGULATION
    )
    
    # Valida e converte o dicionário de volta para o objeto Pydantic para o FastAPI
    return ComplianceChecklist(**result_dict)