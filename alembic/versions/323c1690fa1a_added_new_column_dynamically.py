"""Added new column dynamically

Revision ID: 323c1690fa1a
Revises: 987b6bf93722
Create Date: 2025-01-21 19:51:21.956979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '323c1690fa1a'
down_revision: Union[str, None] = '987b6bf93722'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
