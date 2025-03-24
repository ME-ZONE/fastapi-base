"""generate superuser

Revision ID: a9ccb3ce063c
Revises: 5bf88cdb13d7
Create Date: 2025-03-20 15:16:53.237138

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

import pytz
from alembic import op
from sqlalchemy import text

from app.common.enums import RoleEnum
from app.utils import hash_data

# revision identifiers, used by Alembic.
revision: str = 'a9ccb3ce063c'
down_revision: Union[str, None] = '5bf88cdb13d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

superuser = 'superuser'


def upgrade() -> None:
    connection = op.get_bind()
    hashed_password = hash_data(superuser)

    insert_query = text("""
        INSERT INTO pcs_users (id, username, hashed_password, is_superuser, is_active, role, token_version, created_at, updated_at)
        VALUES (:id, :username, :hashed_password, :is_superuser, :is_active, :role, :token_version, :created_at, :updated_at)
    """)

    connection.execute(insert_query, {
        'id': uuid.uuid4(),
        'username': superuser,
        'hashed_password': hashed_password,
        'is_superuser': True,
        'is_active': True,
        'role': RoleEnum.ADMIN,
        'token_version': 0,
        'created_at': datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
        'updated_at': datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
    })

    print(f"Username:::::{superuser}")
    print(f"Password:::::{superuser}")


def downgrade() -> None:
    connection = op.get_bind()

    delete_query = text("""
        DELETE FROM pcs_users WHERE username = :username
    """)

    connection.execute(delete_query, {
        'username': superuser
    })
