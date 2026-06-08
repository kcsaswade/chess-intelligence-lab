"""Search stats display panel."""


from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout, QWidget

from chesslab.gui.viewmodels import SearchStatsModel


class SearchStatsPanel(QFrame):
    """Displays latest search statistics."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("PanelCard")

        root = QVBoxLayout(self)
        title = QLabel("Search")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        form = QFormLayout()
        self.nodes_value = QLabel("-")
        self.cutoffs_value = QLabel("-")
        self.depth_value = QLabel("-")
        self.time_value = QLabel("-")
        self.pv_value = QLabel("-")
        self.pv_value.setWordWrap(True)

        form.addRow("Nodes:", self.nodes_value)
        form.addRow("Cutoffs:", self.cutoffs_value)
        form.addRow("Depth:", self.depth_value)
        form.addRow("Time (ms):", self.time_value)
        form.addRow("PV:", self.pv_value)
        root.addLayout(form)

    def update_model(self, model: SearchStatsModel) -> None:
        self.nodes_value.setText(model.nodes)
        self.cutoffs_value.setText(model.cutoffs)
        self.depth_value.setText(model.depth)
        self.time_value.setText(model.time_ms)
        self.pv_value.setText(model.pv)