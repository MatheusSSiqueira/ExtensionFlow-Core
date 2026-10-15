from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.domain import ComplianceRequest, ComplianceChecklist
from app.agents.compliance import analyze_compliance
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/validate", response_model=ComplianceChecklist)
async def validate_activity(
    request: ComplianceRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await analyze_compliance(request, db)
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