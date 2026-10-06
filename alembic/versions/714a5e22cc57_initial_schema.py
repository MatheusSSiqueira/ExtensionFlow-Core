"""initial schema

Revision ID: 714a5e22cc57
Revises: 
Create Date: 2026-10-06 14:18:51.246686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '714a5e22cc57'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'students',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'admins',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'activities',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('titulo', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'student_documents',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('student_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('activity_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('arquivo_url', sa.String(length=2048), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id']),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'evaluation_rules',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('activity_id', sa.Uuid(as_uuid=True), nullable=True),
        sa.Column('criterio', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'conversation_memories',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('student_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('conteudo', sa.Text(), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('conversation_memories')
    op.drop_table('evaluation_rules')
    op.drop_table('student_documents')
    op.drop_table('activities')
    op.drop_table('admins')
    op.drop_table('students')
