"""Evaluation breakdown panel."""


from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class EvalPanel(QFrame):
    """Displays evaluation totals and components."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("PanelCard")

        layout = QVBoxLayout(self)
        title = QLabel("Evaluation")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        self.table = QTableWidget(0, 2, self)
        self.table.setHorizontalHeaderLabels(["Component", "Score"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        layout.addWidget(self.table)

    def set_lines(self, lines: list[tuple[str, str]]) -> None:
        self.table.setRowCount(len(lines))
        for row_index, (name, value) in enumerate(lines):
            name_item = QTableWidgetItem(name)
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 0, name_item)
            self.table.setItem(row_index, 1, value_item)