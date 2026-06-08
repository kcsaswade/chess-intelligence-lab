"""Application bootstrap for the PySide6 GUI."""


from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from chesslab.errors import GuiStartupError
from chesslab.gui.main_window import MainWindow
from chesslab.gui.theme import build_application_stylesheet


def main() -> int:
    """Launch the GUI application."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Chess Intelligence Laboratory")
        app.setStyleSheet(build_application_stylesheet())
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as exc:  # pragma: no cover
        raise GuiStartupError("Failed to start ChessLab GUI.") from exc


if __name__ == "__main__":
    raise SystemExit(main())