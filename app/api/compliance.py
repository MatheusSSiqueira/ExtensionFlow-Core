from fastapi import APIRouter
from app.schemas.compliance import ComplianceRequest, ComplianceChecklist
from app.agents.compliance_agent import analyze_compliance_with_gemini
from app.rag.vector_store import vector_db 

router = APIRouter()

@router.post("/validate", response_model=ComplianceChecklist)
def validate_activity_endpoint(request: ComplianceRequest):
    # Busca a regra no banco de dados ChromaDB
    relevant_context = vector_db.search(query_text=request.activity_description)
    
    # ---------------------------------------------------------
    # Imprime no terminal o que o ChromaDB encontrou!
    print("\n--- INÍCIO DO CONTEXTO ENCONTRADO NO RAG ---")
    print(relevant_context)
    print("--- FIM DO CONTEXTO ---\n")
    # ---------------------------------------------------------
    
    # Envia a atividade e a regra para o Gemini
    result_dict = analyze_compliance_with_gemini(
        activity_description=request.activity_description,
        regulation_context=relevant_context
    )
    
    return ComplianceChecklist(**result_dict)