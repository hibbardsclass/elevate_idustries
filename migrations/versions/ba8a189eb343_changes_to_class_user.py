"""changes to Class User

Revision ID: ba8a189eb343
Revises: cfcad9f086ff
Create Date: 2024-06-02 20:42:00.560903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8a189eb343'
down_revision = 'cfcad9f086ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=80), nullable=False))

    # ### end Alembic commands ###
