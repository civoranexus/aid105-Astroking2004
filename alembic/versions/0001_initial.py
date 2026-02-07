"""initial

Revision ID: 0001
Revises: 
Create Date: 2026-01-09 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('external_id', sa.String(length=128), unique=True, nullable=True),
        sa.Column('name', sa.String(length=256), nullable=True),
        sa.Column('email', sa.String(length=256), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('income', sa.Numeric(), nullable=True),
        sa.Column('state', sa.String(length=128), nullable=True),
        sa.Column('district', sa.String(length=128), nullable=True),
        sa.Column('needs', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'schemes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('scheme_id', sa.String(length=64), unique=True, nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('benefits', sa.JSON(), nullable=True),
        sa.Column('documents', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('schemes')
    op.drop_table('users')
