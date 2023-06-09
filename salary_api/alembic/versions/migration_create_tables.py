"""create tables

Revision ID: 7867e260ca03
Revises: 
Create Date: 2023-06-06 22:20:37.623799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7867e260ca03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('job_title', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('salary',
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False, sqlite_on_conflict_unique='REPLACE'),
    sa.Column('next_increase_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('employee_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salary')
    op.drop_table('user')
    # ### end Alembic commands ###
