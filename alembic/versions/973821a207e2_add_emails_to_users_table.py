"""Add_email_field_to_the_users_model

Revision ID: 973821a207e2
Revises: f8091842efed
Create Date: 2023-12-16 13:51:53.850432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '973821a207e2'
down_revision: Union[str, None] = 'f8091842efed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'email')
