"""Add is_setup_complete column

Revision ID: f8091842efed
Revises: 
Create Date: 2023-11-20 18:41:45.204668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f8091842efed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add a new column 'is_setup_complete' to the 'games' table
    op.add_column('games', sa.Column('is_setup_complete', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade():
    # Remove the 'is_setup_complete' column from the 'games' table
    op.drop_column('games', 'is_setup_complete')
