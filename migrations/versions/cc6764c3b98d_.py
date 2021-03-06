"""empty message

Revision ID: cc6764c3b98d
Revises: fb95ebf4fa04
Create Date: 2019-12-11 19:27:03.681607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc6764c3b98d'
down_revision = 'fb95ebf4fa04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('members_name_key', 'members', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('members_name_key', 'members', ['name'])
    op.drop_table('posts')
    # ### end Alembic commands ###
