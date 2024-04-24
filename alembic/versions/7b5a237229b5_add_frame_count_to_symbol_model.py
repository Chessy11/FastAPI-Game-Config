"""add_frame_count_to_symbol_model

Revision ID: 7b5a237229b5
Revises: caf24dd44d45
Create Date: 2024-01-05 20:19:06.320292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b5a237229b5'
down_revision: Union[str, None] = 'caf24dd44d45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('symbols', sa.Column('frame_count', sa.Integer(), nullable=True))



def downgrade() -> None:
    op.drop_column('symbols', 'frame_count')
