import importlib


def test_import_chesslab() -> None:
    module = importlib.import_module("chesslab")
    assert module is not None


def test_import_cli_main() -> None:
    module = importlib.import_module("chesslab.cli.main")
    assert module is not None


def test_import_gui_main_window() -> None:
    module = importlib.import_module("chesslab.gui.main_window")
    assert module is not None