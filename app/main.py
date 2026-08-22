from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.compliance import router as compliance_router # NOVO: Importa a rota

app = FastAPI(
    title="ExtensionFlow API",
    description="API para o assistente multiagente de atividades acadêmicas da Unicesumar",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Conecta a rota na aplicação com um prefixo limpo
app.include_router(compliance_router, prefix="/api/v1/compliance", tags=["Compliance"])

@app.get("/")
def health_check():
    return {"status": "online", "message": "API do ExtensionFlow rodando. Pronta para validações acadêmicas."}