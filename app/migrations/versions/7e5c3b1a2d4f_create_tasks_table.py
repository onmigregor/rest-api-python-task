"""
Revision ID: 7e5c3b1a2d4f
Revises: 5a7d4b2e8c9f_create_revoked_tokens_table
Create Date: 2025-07-29 11:03:00
"""

revision = '7e5c3b1a2d4f'
down_revision = '5a7d4b2e8c9f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import enum

class PriorityEnum(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('priority', sa.Enum('high', 'medium', 'low', name='priorityenum'), nullable=False, server_default='medium'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('assigned_to', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

def downgrade():
    op.drop_table('tasks')
    op.execute('DROP TYPE IF EXISTS priorityenum')
