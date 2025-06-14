"""update location entity

Revision ID: ae3b7c38f3fb
Revises: 5ac9e13537ed
Create Date: 2025-06-02 09:18:22.412062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae3b7c38f3fb'
down_revision = '5ac9e13537ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.String(length=255), nullable=False),
    sa.Column('lng', sa.String(length=255), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('profile_id')
    )
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', mysql.VARCHAR(length=255), nullable=True))

    op.drop_table('location')
    # ### end Alembic commands ###
