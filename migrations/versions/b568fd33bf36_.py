"""empty message

Revision ID: b568fd33bf36
Revises: 7f009a8ee432
Create Date: 2019-12-15 22:12:22.915810

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b568fd33bf36'
down_revision = '7f009a8ee432'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('dateEvent', sa.DateTime(), nullable=True))
    op.drop_column('event', 'created_at')
    op.drop_column('event', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_column('event', 'dateEvent')
    # ### end Alembic commands ###