"""add student row level security

Revision ID: 2b592aa14948
Revises: 714a5e22cc57
Create Date: 2026-10-06 14:24:03.202207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b592aa14948'
down_revision: Union[str, Sequence[str], None] = '714a5e22cc57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # A aplicação deve executar "SET app.current_student_id = '<student UUID>'"
    # no início de cada requisição autenticada, dentro da transação da sessão
    # do banco. Prefira SET LOCAL para que o valor seja descartado ao finalizar
    # a transação e nunca seja reutilizado por outra requisição.
    op.execute("ALTER TABLE student_documents ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE conversation_memories ENABLE ROW LEVEL SECURITY")

    op.execute(
        """
        CREATE POLICY student_documents_student_select
        ON student_documents
        FOR SELECT
        USING (student_id = current_setting('app.current_student_id')::uuid)
        """
    )
    op.execute(
        """
        CREATE POLICY student_documents_student_insert
        ON student_documents
        FOR INSERT
        WITH CHECK (student_id = current_setting('app.current_student_id')::uuid)
        """
    )
    op.execute(
        """
        CREATE POLICY conversation_memories_student_select
        ON conversation_memories
        FOR SELECT
        USING (student_id = current_setting('app.current_student_id')::uuid)
        """
    )
    op.execute(
        """
        CREATE POLICY conversation_memories_student_insert
        ON conversation_memories
        FOR INSERT
        WITH CHECK (student_id = current_setting('app.current_student_id')::uuid)
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP POLICY conversation_memories_student_insert ON conversation_memories")
    op.execute("DROP POLICY conversation_memories_student_select ON conversation_memories")
    op.execute("DROP POLICY student_documents_student_insert ON student_documents")
    op.execute("DROP POLICY student_documents_student_select ON student_documents")
    op.execute("ALTER TABLE conversation_memories DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE student_documents DISABLE ROW LEVEL SECURITY")
