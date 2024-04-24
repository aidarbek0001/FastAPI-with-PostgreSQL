"""Change pizza_id to pizza_name in orders

Revision ID: 2e4936b3b352
Revises: 45a446ff3944
Create Date: 2024-04-24 23:48:21.110460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e4936b3b352'
down_revision: Union[str, None] = '45a446ff3944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Сначала добавляем уникальное ограничение на 'name' в таблице 'pizza'
    op.create_unique_constraint('uq_pizza_name', 'pizza', ['name'])

    # Теперь можно добавить столбец 'pizza_name' в 'orders'
    op.add_column('orders', sa.Column('pizza_name', sa.String(255), nullable=True))

    # Заполняем столбец 'pizza_name' на основе существующих 'pizza_id'
    op.execute("""
    UPDATE orders
    SET pizza_name = (SELECT name FROM pizza WHERE id = orders.pizza_id)
    """)

    # Теперь столбец 'pizza_name' можно сделать NOT NULL
    op.alter_column('orders', 'pizza_name', existing_type=sa.String(255), nullable=False)

    # Удаляем столбец 'pizza_id'
    op.drop_column('orders', 'pizza_id')

    # И только после этого добавляем внешний ключ
    op.create_foreign_key('fk_orders_pizza_name', 'orders', 'pizza', ['pizza_name'], ['name'])


def downgrade():
    # Удаляем внешний ключ
    op.drop_constraint('fk_orders_pizza_name', 'orders', type_='foreignkey')

    # Возвращаем столбец 'pizza_id'
    op.add_column('orders', sa.Column('pizza_id', sa.Integer(), nullable=True))

    # Восстанавливаем данные в 'pizza_id' на основе 'pizza_name'
    op.execute("""
    UPDATE orders
    SET pizza_id = (SELECT id FROM pizza WHERE name = orders.pizza_name)
    """)

    # Удаляем столбец 'pizza_name'
    op.drop_column('orders', 'pizza_name')

    # Удаляем уникальное ограничение из таблицы 'pizza'
    op.drop_constraint('uq_pizza_name', 'pizza', type_='unique')

    # Восстанавливаем внешний ключ для 'pizza_id'
    op.create_foreign_key('orders_pizza_id_fkey', 'orders', 'pizza', ['pizza_id'], ['id'])


