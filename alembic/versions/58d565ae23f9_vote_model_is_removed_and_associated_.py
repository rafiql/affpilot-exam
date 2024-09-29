"""Vote model is removed and associated query

Revision ID: 58d565ae23f9
Revises: 9ce57b4a0a74
Create Date: 2024-09-29 15:41:17.437335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58d565ae23f9'
down_revision = '9ce57b4a0a74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='votes_post_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='votes_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id', name='votes_pkey')
    )
    # ### end Alembic commands ###
