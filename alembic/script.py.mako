"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from alembic import op
import sqlalchemy as sa

${imports if imports}

def upgrade():
    ${upgrades if upgrades}


def downgrade():
    ${downgrades if downgrades}
