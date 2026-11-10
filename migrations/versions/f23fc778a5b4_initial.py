"""initial

Revision ID: f23fc778a5b4
Revises:
Create Date: 2026-11-10 18:52:37.818282

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f23fc778a5b4"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
