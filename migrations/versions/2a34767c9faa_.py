"""empty message

Revision ID: 2a34767c9faa
Revises: 7b50477a2b89
Create Date: 2023-03-05 21:27:14.755415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a34767c9faa'
down_revision = '7b50477a2b89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('income_deduction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('trans_date', sa.Date(), nullable=False),
    sa.Column('category', sa.String(length=20), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('income_deduction')
    # ### end Alembic commands ###
