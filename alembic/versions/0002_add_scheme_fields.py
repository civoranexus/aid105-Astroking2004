"""add scheme fields

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to schemes table
    op.add_column('schemes', sa.Column('eligibility', sa.Text(), nullable=True))
    op.add_column('schemes', sa.Column('application', sa.Text(), nullable=True))
    op.add_column('schemes', sa.Column('level', sa.String(length=64), nullable=True))
    op.add_column('schemes', sa.Column('scheme_category', sa.String(length=256), nullable=True))


def downgrade():
    # Remove the columns if rolling back
    op.drop_column('schemes', 'scheme_category')
    op.drop_column('schemes', 'level')
    op.drop_column('schemes', 'application')
    op.drop_column('schemes', 'eligibility')
