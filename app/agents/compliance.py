from app.core.gemini import get_gemini_client, get_default_config
from app.core.config import settings
from app.schemas.domain import ComplianceChecklist, ComplianceRequest
from app.rag.vector_store import vector_db
from google.genai.errors import APIError
import logging

logger = logging.getLogger(__name__)

def analyze_compliance(request: ComplianceRequest) -> ComplianceChecklist:
    client = get_gemini_client()
    
    # Recuperar contexto do RAG
    search_results = vector_db.search(request.activity_description, n_results=5)
    
    # Formatar o contexto de forma clara e auditável
    context_text = ""
    for res in search_results:
        source = res['metadata'].get('source', 'Desconhecido')
        context_text += f"[FONTE]\nDocumento: {source}\n\n[CONTEÚDO]\n{res['content']}\n\n---\n\n"
    
    # Regra de ausência de evidência: se não achar nada, não aprova.
    if not context_text.strip():
        return ComplianceChecklist(
            is_compliant=False,
            status="inconsistente",
            applicable_requirements=[],
            missing_requirements=["Não foi possível encontrar regras aplicáveis no banco de dados."],
            justification="O sistema não encontrou informações nos regulamentos que correspondam à atividade descrita.",
            sources=[],
            status_message="Atividade Não Encontrada"
        )

    # Montar o Prompt com proteção contra injeção e foco na fonte
    prompt = f"""
INSTRUÇÕES DO SISTEMA:
Você é um assistente acadêmico rigoroso da Unicesumar responsável por auditar atividades de extensão.
Sua tarefa é cruzar a descrição da atividade do aluno com as regras dos documentos recuperados.
- NUNCA invente regras, datas ou documentos.
- NUNCA assuma conformidade se faltar uma evidência exigida na regra (Ex: Ficha de frequência, imagens, termos).
- Baseie-se EXCLUSIVAMENTE nos documentos fornecidos em [DOCUMENTOS RECUPERADOS].
- Se a atividade não estiver em conformidade, liste exatamente o que falta em 'missing_requirements'.

[DOCUMENTOS RECUPERADOS]
{context_text}

[DADOS DO USUÁRIO - ATIVIDADE E EVIDÊNCIAS]
{request.activity_description}
"""
    
    # Força a saída estruturada usando oschema do Pydantic
    config = get_default_config(response_schema=ComplianceChecklist)
    
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=config,
        )
        
        # Validação e converção para o objeto Python
        return ComplianceChecklist.model_validate_json(response.text)
        
    except APIError as e:
        logger.error(f"Erro na API Gemini: {str(e)}")
        raise Exception("Erro de comunicação com o modelo de IA.")
    except Exception as e:
        logger.error(f"Erro de validação ou estrutura: {str(e)}")
        raise Exception("Erro ao processar a análise da atividade.")