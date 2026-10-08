from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.compliance import router as compliance_router
from app.api.auth import router as auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Plataforma de assistência por IA para atividades extensionistas.",
    version="3.0.0",
)

# Configuração de CORS dinâmica baseada no ambiente
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os endpoints do agente
app.include_router(compliance_router, prefix="/api/v1/compliance", tags=["Compliance"])
app.include_router(auth_router, tags=["Authentication"])

# Rota para Health Check (Essencial para Kubernetes/Cloud Run)
@app.get("/health", tags=["System"])
def health_check():
    """Endpoint para liveness e readiness probes."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", tags=["UI"])
def serve_frontend():
    return FileResponse("frontend/index.html")