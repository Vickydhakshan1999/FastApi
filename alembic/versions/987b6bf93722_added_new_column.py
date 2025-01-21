"""Added new column

Revision ID: 987b6bf93722
Revises: d5216f60e8cb
Create Date: 2025-01-21 19:40:08.237116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '987b6bf93722'
down_revision: Union[str, None] = 'd5216f60e8cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
