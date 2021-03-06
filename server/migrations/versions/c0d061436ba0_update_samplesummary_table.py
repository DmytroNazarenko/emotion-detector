"""update samplesummary table

Revision ID: c0d061436ba0
Revises: 
Create Date: 2019-05-28 13:35:16.226891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0d061436ba0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample_summary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summary_id', sa.Integer(), nullable=True),
    sa.Column('neutral', sa.Float(), nullable=True),
    sa.Column('happy', sa.Float(), nullable=True),
    sa.Column('sad', sa.Float(), nullable=True),
    sa.Column('hate', sa.Float(), nullable=True),
    sa.Column('anger', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['summary_id'], ['summary.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sample_summary')
    # ### end Alembic commands ###
