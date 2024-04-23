"""Add order module

Revision ID: 45a446ff3944
Revises: a113dc683f31
Create Date: 2024-04-23 19:31:40.059930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45a446ff3944'
down_revision: Union[str, None] = 'a113dc683f31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customer_name', sa.String(length=255), nullable=False),
        sa.Column('pizza_id', sa.Integer, sa.ForeignKey('pizza.id'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False, default=1),
        sa.Column('status', sa.Enum('pending', 'preparing', 'ready', 'delivered', name='order_statuses'), default='pending', nullable=False)
    )

def downgrade() -> None:
    op.drop_table('orders')

