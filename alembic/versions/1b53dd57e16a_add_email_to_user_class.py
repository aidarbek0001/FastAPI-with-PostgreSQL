"""add email to User class

Revision ID: 1b53dd57e16a
Revises: 9e31c37dae79
Create Date: 2024-04-25 17:54:31.774676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b53dd57e16a'
down_revision: Union[str, None] = '9e31c37dae79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
