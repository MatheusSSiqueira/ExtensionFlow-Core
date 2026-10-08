"""add pgvector document embeddings

Revision ID: 5f6e7a8b9c01
Revises: 2b592aa14948
"""

from typing import Sequence, Union

from alembic import op


revision: str = "5f6e7a8b9c01"
down_revision: Union[str, Sequence[str], None] = "2b592aa14948"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(
        """
        CREATE TABLE document_embeddings (
            id TEXT PRIMARY KEY,
            tenant_id UUID NULL,
            document_id TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding vector(768) NOT NULL,
            criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE INDEX document_embeddings_embedding_idx
        ON document_embeddings USING hnsw (embedding vector_cosine_ops)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS document_embeddings_embedding_idx")
    op.execute("DROP TABLE IF EXISTS document_embeddings")