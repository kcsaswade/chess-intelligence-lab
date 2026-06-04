"""Main application window for the GUI shell."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow

from chesslab.constants import APP_WINDOW_TITLE, DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH


class MainWindow(QMainWindow):
    """Minimal main window for Chunk 1."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_WINDOW_TITLE)
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self._build_ui()

    def _build_ui(self) -> None:
        label = QLabel("Chess Intelligence Laboratory")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)