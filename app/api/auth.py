from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Student
from app.db.session import get_db
from app.services.auth import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter()


class AuthRequest(BaseModel):
    email: str
    senha: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def validate_unicesumar_email(cls, email: str) -> str:
        normalized_email = email.strip().lower()
        if not normalized_email.endswith("@unicesumar.edu.br"):
            raise ValueError("O e-mail deve terminar em @unicesumar.edu.br")
        return normalized_email


class RegisterRequest(AuthRequest):
    nome: str = Field(min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    existing_student = await db.scalar(select(Student).where(Student.email == data.email))
    if existing_student is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")

    student = Student(
        email=data.email,
        nome=data.nome,
        senha_hash=hash_password(data.senha),
    )
    db.add(student)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado") from exc

    await db.refresh(student)
    return TokenResponse(access_token=create_access_token(student.id))


@router.post("/auth/login", response_model=TokenResponse)
async def login(data: AuthRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    student = await db.scalar(select(Student).where(Student.email == data.email))
    if student is None or not verify_password(data.senha, student.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=create_access_token(student.id))