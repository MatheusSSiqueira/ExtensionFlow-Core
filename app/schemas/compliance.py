from pydantic import BaseModel, Field

class ComplianceChecklist(BaseModel):
    # O Pydantic força o LLM a preencher este campo PRIMEIRO, obrigando-o a pensar.
    reasoning: str = Field(
        description="Pense passo a passo. Identifique qual artigo do regulamento se aplica a esta atividade específica. Depois analise se a regra foi cumprida com as evidências apresentadas."
    )
    is_compliant: bool = Field(description="True se a atividade atende a todas as regras daquele artigo.")
    missing_requirements: list[str] = Field(
        default_factory=list, 
        description="Lista de itens faltantes. Retorne vazio se estiver tudo certo."
    )
    status_message: str = Field(description="Mensagem curta e clara para o aluno.")

class ComplianceRequest(BaseModel):
    activity_description: str = Field(..., description="A descrição da atividade que o usuário quer fazer.")