from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ExtensionFlow API",
    description="API para o assistente multiagente de atividades acadêmicas da Unicesumar",
    version="2.0.0",
)

# Configuração de CORS (Segurança): Permite que o frontend converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, mudaremos isso para a URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    Não expõe lógicas de agentes, apenas confirma que o servidor está no ar.
    """
    return {
        "status": "online", 
        "message": "API do ExtensionFlow rodando. Pronta para validações acadêmicas."
    }