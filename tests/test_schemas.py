import pytest
from pydantic import BaseModel, Field, ValidationError

class ComplianceChecklist(BaseModel):
    is_compliant: bool = Field(..., description="True se atende a todas as regras.")
    missing_requirements: list[str] = Field(default_factory=list, description="O que falta.")
    status_message: str = Field(..., description="Mensagem clara ao usuário.")

def test_compliance_checklist_valid_creation():
    """Testa se o schema é criado corretamente com dados válidos."""
    data = {
        "is_compliant": False,
        "missing_requirements": ["Falta certificado de participação", "Carga horária insuficiente"],
        "status_message": "Sua atividade não atende aos requisitos mínimos."
    }
    
    checklist = ComplianceChecklist(**data)
    
    assert checklist.is_compliant is False
    assert len(checklist.missing_requirements) == 2
    assert "Falta certificado" in checklist.missing_requirements[0]

def test_compliance_checklist_missing_required_fields():
    """Testa se o schema bloqueia a criação quando faltam campos obrigatórios."""
    data = {
        "is_compliant": True
    }
    
    with pytest.raises(ValidationError):
        ComplianceChecklist(**data)