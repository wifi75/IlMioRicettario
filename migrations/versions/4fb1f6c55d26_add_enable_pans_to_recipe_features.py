"""Add enable_pans to recipe_features

Revision ID: 4fb1f6c55d26
Revises: 56e958a68bc7
Create Date: 2026-06-11 08:34:12.240369
"""

from alembic import op
import sqlalchemy as sa


revision = '4fb1f6c55d26'
down_revision = '56e958a68bc7'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('recipe_features') as batch_op:
        batch_op.add_column(
            sa.Column(
                'enable_pans',
                sa.Boolean(),
                nullable=True
            )
        )


def downgrade():

    with op.batch_alter_table('recipe_features') as batch_op:
        batch_op.drop_column('enable_pans')