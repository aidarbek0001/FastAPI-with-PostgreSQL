"""Add primary key 'id' to 'users' table

Revision ID: da6bc974a741
Revises: 29ada16760c4
Create Date: 2024-04-18 15:14:13.676574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da6bc974a741'
down_revision = '29ada16760c4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('id', sa.Integer, primary_key=True))


def downgrade():
    op.drop_column('users', 'id')
