"""Composite side panel for game info and search data."""


from __future__ import annotations

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from chesslab.gui.eval_panel import EvalPanel
from chesslab.gui.game_info_widget import GameInfoWidget
from chesslab.gui.move_list_widget import MoveListWidget
from chesslab.gui.search_stats_panel import SearchStatsPanel


class SidePanel(QFrame):
    """Stacks secondary game information widgets."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("SidePanelFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.game_info_widget = GameInfoWidget(self)
        self.eval_panel = EvalPanel(self)
        self.search_stats_panel = SearchStatsPanel(self)
        self.move_list_widget = MoveListWidget(self)

        layout.addWidget(self.game_info_widget)
        layout.addWidget(self.eval_panel, stretch=2)
        layout.addWidget(self.search_stats_panel)
        layout.addWidget(self.move_list_widget, stretch=1)