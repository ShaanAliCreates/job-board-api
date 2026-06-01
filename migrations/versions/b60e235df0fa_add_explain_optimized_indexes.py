"""add_explain_optimized_indexes

Revision ID: b60e235df0fa
Revises: 239bac83e45d
Create Date: 2026-05-31 10:47:21.228423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b60e235df0fa'
down_revision: Union[str, Sequence[str], None] = '239bac83e45d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_jobs_status_created','jobs',['status','created_at'])
    op.create_index('idx_jobs_location','jobs',['location'])
    op.create_index('idx_jobs_active_created','jobs',['created_at'],postgresql_where=sa.text("status='active'"))




def downgrade() -> None:
    op.drop_index('idx_jobs_status_created',table_name='jobs')
    op.drop_index('idx_jobs_location',table_name='jobs')
    op.drop_index('idx_jobs_active_created',table_name='jobs')
    