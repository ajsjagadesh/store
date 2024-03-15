"""create_admin_table

Revision ID: 24e7eaab2b94
Revises: f14328e022d4
Create Date: 2024-03-04 16:34:46.728937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24e7eaab2b94'
down_revision: Union[str, None] = 'f14328e022d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
