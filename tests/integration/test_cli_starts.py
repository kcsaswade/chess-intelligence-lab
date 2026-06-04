from chesslab.cli.main import build_startup_message, main


def test_build_startup_message_contains_name() -> None:
    message = build_startup_message()
    assert "Chess Intelligence Laboratory" in message
    assert "Version:" in message


def test_cli_main_returns_zero() -> None:
    assert main() == 0