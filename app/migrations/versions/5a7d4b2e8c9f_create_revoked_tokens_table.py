"""
Revision ID: 5a7d4b2e8c9f
Revises: 3f1d8b9c6a45_create_user_roles_table
Create Date: 2025-07-29 02:35:00
"""

revision = '5a7d4b2e8c9f'
down_revision = '002_create_user_roles_table'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'revoked_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('jti', sa.String(length=255), unique=True, nullable=False),
        sa.Column('token', sa.String(length=512), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True)
    )

def downgrade():
    op.drop_table('revoked_tokens')
