"""create_applications

Revision ID: d5cc9c61e687
Revises: 1d957a634285
Create Date: 2026-05-21 04:34:23.638561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5cc9c61e687'
down_revision: Union[str, Sequence[str], None] = '1d957a634285'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('applications',
                    sa.Column('id',sa.Integer(), primary_key=True),
                    sa.Column('job_id',sa.Integer(), sa.ForeignKey('jobs.id', ondelete='CASCADE')),
                    sa.Column('applicant_id',sa.Integer(),sa.ForeignKey('applicants.id',ondelete='CASCADE')),
                    sa.Column('status',sa.String(20),server_default='applied'),
                    sa.Column('applied_at',sa.TIMESTAMP(), server_default=sa.text('Now()')),
                    sa.Column('update_at',sa.TIMESTAMP(),server_default=sa.text('NOW()')),
                    sa.UniqueConstraint('job_id','applicant_id',name='uq_jobId_applicant_id')
                    )


def downgrade() -> None:
    op.drop_table('applications')