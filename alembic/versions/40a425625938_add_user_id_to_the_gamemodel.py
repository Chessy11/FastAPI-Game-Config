"""add user_id to the GameModel

Revision ID: 40a425625938
Revises: 973821a207e2
Create Date: 2023-12-16 20:09:43.879782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a425625938'
down_revision: Union[str, None] = '973821a207e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column('games', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_games_user_id', 'games', 'users', ['user_id'], ['user_id'])
    op.alter_column('games', 'user_id', nullable=True)



def downgrade():
    op.drop_constraint('fk_games_user_id', 'games', type_='foreignkey')
    op.drop_column('games', 'user_id')
