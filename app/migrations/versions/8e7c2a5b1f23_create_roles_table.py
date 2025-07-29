"""
Revision ID: 001_create_roles_table
Revises: dfa4fd48a318
Create Date: 2025-07-29 02:10:00
"""

revision = '001_create_roles_table'
down_revision = 'dfa4fd48a318'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), unique=True, nullable=False)
    )

def downgrade():
    op.drop_table('roles')
