"""add_indexes

Revision ID: 239bac83e45d
Revises: d5cc9c61e687
Create Date: 2026-05-21 04:34:38.646405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '239bac83e45d'
down_revision: Union[str, Sequence[str], None] = 'd5cc9c61e687'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_jobs_company_id', 'jobs',['company_id'])
    op.create_index('idx_jobs_status','jobs',['status'])
    op.create_index('idx_jobs_created_at','jobs',['created_at'])

    op.create_index('idx_applications_job_id','applications',['job_id'])
    op.create_index('idx_applications_skill_id','applications',['applicant_id'])
    op.create_index('idx_applications_status','applications',['status'])

def downgrade() -> None:
    op.drop_index('idx_jobs_company_id', table_name='jobs')
    op.drop_index('idx_jobs_status', table_name='jobs')
    op.drop_index('idx_jobs_created_at', table_name='jobs')
    op.drop_index('idx_applications_job_id',table_name='applications')
    op.drop_index('idx_applications_skill_id',table_name='applications')
    op.drop_index('idx_applications_status',table_name='applications')
