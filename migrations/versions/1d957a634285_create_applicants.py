"""create_applicants

Revision ID: 1d957a634285
Revises: 7adc101949a7
Create Date: 2026-05-21 04:33:56.742673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d957a634285'
down_revision: Union[str, Sequence[str], None] = '7adc101949a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('applicants',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('name',sa.String(200),nullable=False),
                    sa.Column('email',sa.String(150), nullable=False,unique=True),
                    sa.Column('created_at',sa.TIMESTAMP(), server_default=sa.text('Now()'))

                    )


def downgrade() -> None:
    op.drop_table('applicants')
