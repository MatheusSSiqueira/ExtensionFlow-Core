from pydantic import BaseModel, Field
from typing import List, Literal

class ComplianceChecklist(BaseModel):
    is_compliant: bool = Field(..., description="Verdadeiro apenas se a atividade atende a todos os requisitos sem pendências.")
    status: Literal["conforme", "pendente", "inconsistente"] = Field(..., description="Estado atual da análise.")
    applicable_requirements: List[str] = Field(..., description="Lista de requisitos do regulamento que se aplicam a esta atividade.")
    missing_requirements: List[str] = Field(..., description="O que falta para a atividade ser aprovada. Retornar vazio se conforme.")
    justification: str = Field(..., description="Justificativa direta, clara e útil ao usuário. Sem raciocínio interno.")
    sources: List[str] = Field(..., description="Nome do documento e seção onde a regra foi encontrada. Ex: ['Ficha de Frequência', 'Regulamento de Extensão - Art. 2'].")
    status_message: str = Field(..., description="Mensagem curta de status que será exibida como título no frontend.")

class ComplianceRequest(BaseModel):
    activity_description: str = Field(..., min_length=10, description="Descrição da atividade e dos documentos apresentados pelo aluno.")