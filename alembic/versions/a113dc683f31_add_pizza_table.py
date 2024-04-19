"""Add pizza table

Revision ID: a113dc683f31
Revises: da6bc974a741
Create Date: 2024-04-19 14:25:42.710185

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a113dc683f31'
down_revision = 'da6bc974a741'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'pizza',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('price', sa.Integer, nullable=False)
    )

def downgrade():
    op.drop_table('pizza')
