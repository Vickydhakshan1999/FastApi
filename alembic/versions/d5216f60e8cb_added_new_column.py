"""Added new column

Revision ID: d5216f60e8cb
Revises: 51cba76a6a6b
Create Date: 2025-01-21 19:33:14.311899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5216f60e8cb'
down_revision: Union[str, None] = '51cba76a6a6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('your_table_name', sa.Column('new_column', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('your_table_name', 'new_column')

