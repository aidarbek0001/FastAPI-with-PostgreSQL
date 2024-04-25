"""add roles

Revision ID: 9e31c37dae79
Revises: 2e4936b3b352
Create Date: 2024-04-25 13:05:40.299244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e31c37dae79'
down_revision: Union[str, None] = '2e4936b3b352'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(length=255), nullable=True))
    op.execute("UPDATE users SET role = 'customer' WHERE role IS NULL")
    op.alter_column('users', 'role', existing_type=sa.String(length=255), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
