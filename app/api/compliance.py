from fastapi import APIRouter
from app.schemas.compliance import ComplianceRequest, ComplianceChecklist
from app.agents.compliance_agent import analyze_compliance_with_gemini
from app.rag.vector_store import vector_db 

router = APIRouter()

@router.post("/validate", response_model=ComplianceChecklist)
def validate_activity_endpoint(request: ComplianceRequest):
    # Recupera trechos relevantes do regulamento usando o RAG (ChromaDB)
    relevant_context = vector_db.search(query_text=request.activity_description)

    # Log para desenvolvimento: mostra o contexto usado na consulta ao LLM
    print("\n--- CONTEXTO RECUPERADO PELO RAG ---")
    print(relevant_context)
    print("--- FIM DO CONTEXTO ---\n")

    # Chama o agente que interage com o Gemini, fornecendo atividade e contexto
    result_dict = analyze_compliance_with_gemini(
        activity_description=request.activity_description,
        regulation_context=relevant_context
    )
    
    return ComplianceChecklist(**result_dict)