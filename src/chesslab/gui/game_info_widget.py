"""Game info panel widget."""


from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout, QWidget

from chesslab.gui.viewmodels import GameInfoModel


class GameInfoWidget(QFrame):
    """Displays high-level game state."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("PanelCard")

        root = QVBoxLayout(self)
        title = QLabel("Game")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        form = QFormLayout()
        self.side_value = QLabel("-")
        self.status_value = QLabel("-")
        self.result_value = QLabel("*")
        self.engine_value = QLabel("-")

        form.addRow("Side to move:", self.side_value)
        form.addRow("Status:", self.status_value)
        form.addRow("Result:", self.result_value)
        form.addRow("Engine:", self.engine_value)
        root.addLayout(form)

    def update_model(self, model: GameInfoModel) -> None:
        self.side_value.setText(model.side_to_move)
        self.status_value.setText(model.status_text)
        self.result_value.setText(model.result_text)
        self.engine_value.setText(model.engine_state_text)