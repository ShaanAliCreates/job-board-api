"""add_company_auth

Revision ID: fbf3e88a342c
Revises: 16d9d4da3e61
Create Date: 2026-07-02 10:54:17.627446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbf3e88a342c'
down_revision: Union[str, Sequence[str], None] = '16d9d4da3e61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('companies',sa.Column('password_hash',sa.String(255)))
    op.add_column('companies',sa.Column('role',sa.String(255),server_default='recruiter'))


def downgrade() -> None:
    op.drop_column('companies','role')
    op.drop_column('companies','password_hash')


