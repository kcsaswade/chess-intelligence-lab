"""Promotion selection dialog for human moves."""


from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from chesslab.engine.piece import PieceType


class PromotionDialog(QDialog):
    """Modal dialog for choosing a promotion piece."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Choose promotion")
        self._selected_piece: PieceType | None = None

        layout = QVBoxLayout(self)
        buttons_layout = QHBoxLayout()

        for label, piece_type in (
            ("Queen", PieceType.QUEEN),
            ("Rook", PieceType.ROOK),
            ("Bishop", PieceType.BISHOP),
            ("Knight", PieceType.KNIGHT),
        ):
            button = QPushButton(label, self)
            button.clicked.connect(self._make_selection(piece_type))
            buttons_layout.addWidget(button)

        layout.addLayout(buttons_layout)

        cancel_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel, self)
        cancel_box.rejected.connect(self.reject)
        layout.addWidget(cancel_box)

    def _make_selection(self, piece_type: PieceType) -> Callable[[], None]:
        def handler() -> None:
            self._selected_piece = piece_type
            self.accept()

        return handler

    @property
    def selected_piece(self) -> PieceType | None:
        return self._selected_piece

    @classmethod
    def choose_promotion(cls, parent: QWidget | None = None) -> PieceType | None:
        dialog = cls(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.selected_piece
        return None