"""Ponto de entrada da aplicação FastAPI.

Serve a API REST e os arquivos estáticos do frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.compliance import router as compliance_router


app = FastAPI(
    title="ExtensionFlow API",
    description="API para o assistente multiagente de atividades acadêmicas",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compliance_router, prefix="/api/v1/compliance", tags=["Compliance"])

# Monta a pasta do frontend para servir os arquivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Rota principal para a interface visual (HTML)
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")