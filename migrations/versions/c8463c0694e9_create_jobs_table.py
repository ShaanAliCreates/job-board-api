"""create_jobs_table

Revision ID: c8463c0694e9
Revises: 6352c9f4e445
Create Date: 2026-05-21 04:32:50.413477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8463c0694e9'
down_revision: Union[str, Sequence[str], None] = '6352c9f4e445'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('jobs',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title',sa.String(200) ,nullable=False),
                    sa.Column('location',sa.String(100)),
                    sa.Column('created_at',sa.TIMESTAMP(),server_default=sa.text('NOW()')),
                    sa.Column('company_id',sa.Integer() ,sa.ForeignKey('companies.id',ondelete='CASCADE')),
                    sa.Column('description',sa.Text()),
                    sa.Column('salary_min',sa.Integer()),
                    sa.Column('salary_max',sa.Integer()),
                    sa.Column('is_remote',sa.Boolean(),server_default='False'),
                    sa.Column('status',sa.String(50),server_default='active')
                    )


def downgrade() -> None:
    op.drop_table('jobs')
