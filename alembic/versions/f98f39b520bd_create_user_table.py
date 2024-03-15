"""create_user_table

Revision ID: f98f39b520bd
Revises: 
Create Date: 2024-03-02 13:41:33.707213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'f98f39b520bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_details',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(200), unique=True, index=True),
        sa.Column("mobile_number", sa.String(20)),
        sa.Column('hashed_password', sa.String(200)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('address', sa.String(1500), nullable=False),
        sa.Column('land_mark', sa.String(500)),
        sa.Column('pincode', sa.String(20), nullable=False),
        sa.Column('disabled', sa.Boolean, default=False, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('user_details')
