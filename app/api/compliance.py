from fastapi import APIRouter, HTTPException
from app.schemas.domain import ComplianceRequest, ComplianceChecklist
from app.agents.compliance import analyze_compliance
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/validate", response_model=ComplianceChecklist)
def validate_activity(request: ComplianceRequest):
    try:
        result = analyze_compliance(request)
        return result
    except Exception as e:
        logger.error(f"Falha no endpoint /validate: {str(e)}")
        # Nunca retorna Stack Trace parar o usuário, retorna um payload limpo
        raise HTTPException(
            status_code=503,
            detail={
                "code": "ANALYSIS_UNAVAILABLE",
                "message": "O serviço de análise está temporariamente indisponível ou encontrou um erro."
            }
        )