"""add_image_url_and_animation_url_to_symbols_table

Revision ID: caf24dd44d45
Revises: 40a425625938
Create Date: 2024-01-05 11:47:37.545228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caf24dd44d45'
down_revision: Union[str, None] = '40a425625938'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('symbols', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('symbols', sa.Column('animation_url', sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_column('symbols', 'image_url')
    op.drop_column('symbols', 'animation_url')
