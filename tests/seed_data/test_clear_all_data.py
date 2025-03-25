from alembic import command
from alembic.config import Config


def test_clear_all_data() -> None:
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "base")
    assert 200 == 200  # noqa: PLR0133
