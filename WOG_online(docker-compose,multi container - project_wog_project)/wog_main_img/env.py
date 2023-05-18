"""Initial migration.

Revision ID: 1
Revises: 
Create Date: 2023-04-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_scores_table',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(20), nullable=True),
        sa.Column('score', sa.Integer, nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True)
    )


def downgrade():
    op.drop_table('user_scores_table')
