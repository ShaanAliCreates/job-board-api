"""add_auth_to_applicants

Revision ID: 16d9d4da3e61
Revises: b60e235df0fa
Create Date: 2026-06-22 12:13:02.559188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16d9d4da3e61'
down_revision: Union[str, Sequence[str], None] = 'b60e235df0fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applicants',sa.Column('password_hash',sa.String(255)))
    op.add_column('applicants',sa.Column('is_active',sa.Boolean(),server_default='True'))


    op.create_table('refresh_tokens',
                    sa.Column('id',sa.Integer(),primary_key=True),
                    sa.Column('applicant_id' ,sa.Integer(),sa.ForeignKey('applicants.id',ondelete='CASCADE')),
                    sa.Column('token_hash',sa.String(255),unique=True),
                    sa.Column('expery_date',sa.TIMESTAMP()),
                    sa.Column('created_at',sa.TIMESTAMP(),server_default=sa.text('NOW()'))
                    )


def downgrade() -> None:
    op.drop_table('refresh_tokens')
    op.drop_column('applicants','is_active')
    op.drop_column('applicants','password_hash')
