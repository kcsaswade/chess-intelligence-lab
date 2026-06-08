"""Move list widget for SAN history."""


from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QVBoxLayout, QWidget


class MoveListWidget(QFrame):
    """Displays played SAN moves."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("PanelCard")

        layout = QVBoxLayout(self)
        title = QLabel("Moves")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

    def set_moves(self, san_moves: list[str]) -> None:
        self.list_widget.clear()
        row_index = 0
        while row_index < len(san_moves):
            move_number = (row_index // 2) + 1
            white_move = san_moves[row_index]
            black_move = san_moves[row_index + 1] if row_index + 1 < len(san_moves) else ""
            self.list_widget.addItem(f"{move_number}. {white_move} {black_move}".strip())
            row_index += 2