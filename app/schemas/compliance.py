from pydantic import BaseModel, Field

class ComplianceChecklist(BaseModel):
    is_compliant: bool = Field(description="True se a atividade atende a todas as regras.")
    missing_requirements: list[str] = Field(
        default_factory=list, 
        description="Lista de itens faltantes. Retorne uma lista vazia se estiver tudo certo."
    )
    status_message: str = Field(description="Mensagem curta e clara para o aluno.")

class ComplianceRequest(BaseModel):
    activity_description: str = Field(..., description="A descrição da atividade que o usuário quer fazer.")