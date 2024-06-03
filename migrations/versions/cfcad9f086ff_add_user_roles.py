"""add user roles

Revision ID: cfcad9f086ff
Revises: 9a9b92d170b5
Create Date: 2024-05-28 11:44:30.455891

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'cfcad9f086ff'
down_revision = '9a9b92d170b5'
branch_labels = None
depends_on = None

def table_exists(table_name, connection):
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()

def upgrade():
    # Connect to the current database
    connection = op.get_bind()

    # Check if the 'role' table exists
    if not table_exists('role', connection):
        op.create_table('role',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=64), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_role', 'role', ['role_id'], ['id'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_role', type_='foreignkey')
        batch_op.drop_column('role_id')

    op.drop_table('role')
