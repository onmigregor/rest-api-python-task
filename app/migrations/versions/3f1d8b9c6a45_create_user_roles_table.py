"""
Revision ID: 002_create_user_roles_table
Revises: 001_create_roles_table
Create Date: 2025-07-29 02:11:00
"""

revision = '002_create_user_roles_table'
down_revision = '001_create_roles_table'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('user_roles')
