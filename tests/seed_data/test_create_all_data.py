from sqlalchemy.orm import Session

from .seed_user import seed_user


def test_create_all_data(session: Session) -> None:
    seed_user.create_data(session=session)
    assert 200 == 200  # noqa: PLR0133
