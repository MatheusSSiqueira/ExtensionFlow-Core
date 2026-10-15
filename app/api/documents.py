from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Activity, Student, StudentDocument
from app.db.session import get_db
from app.rag.ingest import ingest_uploaded_document
from app.services.auth import get_current_student


router = APIRouter()


class DocumentUploadResponse(BaseModel):
    document_id: UUID


def save_to_blob_storage(content: bytes, filename: str, student_id: UUID) -> str:
    """Stub para persistência do arquivo em blob storage."""
    return f"blob://pending/{student_id}/{filename}"


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    activity_id: UUID = Form(...),
    file: UploadFile = File(...),
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> DocumentUploadResponse:
    activity_exists = await db.scalar(select(Activity.id).where(Activity.id == activity_id))
    if activity_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atividade não encontrada")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O arquivo enviado está vazio")

    filename = file.filename or "documento"
    arquivo_url = save_to_blob_storage(content, filename, student.id)
    document = StudentDocument(
        student_id=student.id,
        activity_id=activity_id,
        arquivo_url=arquivo_url,
        status="processando",
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    ingest_uploaded_document(
        content=content,
        filename=filename,
        document_id=str(document.id),
        tenant_id=str(student.id),
    )

    document.status = "processado"
    await db.commit()
    return DocumentUploadResponse(document_id=document.id)
