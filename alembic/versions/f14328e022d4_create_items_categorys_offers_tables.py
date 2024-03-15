"""create_items_categorys_offers_tables

Revision ID: f14328e022d4
Revises: f98f39b520bd
Create Date: 2024-03-04 00:14:47.605022

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f14328e022d4'
down_revision: Union[str, None] = 'f98f39b520bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:


    op.create_table(
        'items',
        sa.Column('item_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('item_name', sa.String(500), nullable=True),
        sa.Column('item_description', sa.String(1000)),
        sa.Column('item_quantity', sa.String(50)),
        sa.Column('item_price', sa.Float, nullable=True),
        sa.Column('category', sa.String(200)),
        sa.Column('manufacture_date', sa.Date),
        sa.Column('expiry_date', sa.Date),
        sa.Column('units', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('status', sa.String(100), server_default="Active"),
        sa.Column('last_updated_by', sa.String(200)),
        sa.Column('discount', sa.Float)
    )

    op.create_table(
        'categorys',
        sa.Column('category_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('category_name', sa.String(200), nullable=True, unique=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_by', sa.String(200))
    )

    op.create_table(
        'offers',
        sa.Column('offer_id', sa.Integer, autoincrement=True, primary_key=True,),
        sa.Column('item_id', sa.Integer),
        sa.Column('discount', sa.Float),
         sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_by', sa.String(200))
    )




def downgrade() -> None:
    # op.drop_constraint('offers_ibfk_1', 'offers', type_='foreignkey')
    op.drop_table('items')
    op.drop_table('categorys')
    op.drop_table('offers')
