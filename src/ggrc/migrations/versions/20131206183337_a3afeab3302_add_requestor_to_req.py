
"""Add requestor to Requests

Revision ID: a3afeab3302
Revises: 22917277cc68
Create Date: 2013-12-06 18:33:37.370094

"""

# revision identifiers, used by Alembic.
revision = 'a3afeab3302'
down_revision = '22917277cc68'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('requests', sa.Column('requestor_id', sa.Integer))

def downgrade():
  op.drop_column('requests', 'requestor_id')
