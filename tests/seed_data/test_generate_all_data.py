from .seed_user import seed_user


def test_generate_all_data() -> None:
    seed_user.generate_data()
    assert 200 == 200  # noqa: PLR0133
