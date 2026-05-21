"""create_skills_and_job_skills

Revision ID: 7adc101949a7
Revises: c8463c0694e9
Create Date: 2026-05-21 04:33:36.297301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7adc101949a7'
down_revision: Union[str, Sequence[str], None] = 'c8463c0694e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('skills',
                    sa.Column('id',sa.Integer(), primary_key=True),
                    sa.Column('name',sa.String(100), nullable=False)
                    )
    

    op.create_table('job_skills',
                    sa.Column('job_id',sa.Integer, sa.ForeignKey('jobs.id',ondelete='CASCADE'),primary_key=True),
                    sa.Column('skill_id',sa.Integer,sa.ForeignKey('skills.id',ondelete='CASCADE'),primary_key=True)
                    )


def downgrade() -> None:
    op.drop_table('job_skills')
    op.drop_table('skills')