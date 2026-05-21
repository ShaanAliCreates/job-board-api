"""create_companies_table

Revision ID: 6352c9f4e445
Revises: 
Create Date: 2026-05-21 04:32:36.746725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6352c9f4e445'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('companies',sa.Column('id',sa.Integer(),primary_key=True),
                    sa.Column('name',sa.String(200), nullable=False),
                    sa.Column('email',sa.String(150),nullable=False,unique=True),
                    sa.Column('website',sa.String(300)),
                    sa.Column('is_active', sa.Boolean, server_default='True'),
                    sa.Column('created_at',sa.TIMESTAMP(), server_default=sa.text('NOW()'))
                    )



def downgrade() -> None:
    op.drop_table('companies')
