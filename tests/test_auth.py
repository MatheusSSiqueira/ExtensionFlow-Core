import asyncio
import os
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import ValidationError

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("JWT_SECRET", "test-secret-with-at-least-32-bytes")

from app.api.auth import AuthRequest, RegisterRequest, login
from app.db.models import Student
from app.services.auth import (
    create_access_token,
    get_current_student,
    hash_password,
)


class FakeAsyncSession:
    def __init__(self, student: Student | None = None):
        self.student = student

    async def scalar(self, _query):
        return self.student


def test_register_rejects_non_unicesumar_email():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="student@example.com",
            senha="senha-segura",
            nome="Student",
        )


def test_login_with_wrong_password_returns_401():
    student = Student(
        id=uuid4(),
        email="student@unicesumar.edu.br",
        nome="Student",
        senha_hash=hash_password("senha-correta"),
    )

    with pytest.raises(HTTPException) as error:
        asyncio.run(
            login(
                AuthRequest(
                    email=student.email,
                    senha="senha-incorreta",
                ),
                FakeAsyncSession(student),
            )
        )

    assert error.value.status_code == 401


def test_valid_jwt_token_passes_get_current_student():
    student = Student(
        id=uuid4(),
        email="student@unicesumar.edu.br",
        nome="Student",
        senha_hash=hash_password("senha-segura"),
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=create_access_token(student.id),
    )

    current_student = asyncio.run(
        get_current_student(credentials, FakeAsyncSession(student))
    )

    assert current_student is student
