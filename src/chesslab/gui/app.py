"""Application bootstrap for the PySide6 GUI."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from chesslab.errors import GuiStartupError
from chesslab.gui.main_window import MainWindow


def main() -> int:
    """Launch the GUI application."""
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as exc:  # pragma: no cover - startup guard
        raise GuiStartupError("Failed to start ChessLab GUI.") from exc


if __name__ == "__main__":
    raise SystemExit(main())