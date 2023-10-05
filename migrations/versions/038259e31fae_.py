"""empty message

Revision ID: 038259e31fae
Revises: 49ee4ae16960
Create Date: 2023-10-05 23:39:03.632626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038259e31fae'
down_revision = '49ee4ae16960'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=250),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###
