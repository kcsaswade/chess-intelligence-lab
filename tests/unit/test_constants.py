from chesslab.constants import APP_NAME, APP_WINDOW_TITLE, VERSION_STRING


def test_app_name_defined() -> None:
    assert APP_NAME == "Chess Intelligence Laboratory"


def test_window_title_defined() -> None:
    assert isinstance(APP_WINDOW_TITLE, str)
    assert APP_WINDOW_TITLE


def test_version_string_defined() -> None:
    assert isinstance(VERSION_STRING, str)
    assert VERSION_STRING