"""Background workers for GUI tasks."""


from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from chesslab.engine.position import Position
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.engine.search.result import SearchResult


class SearchWorker(QObject):
    """Runs engine search off the GUI thread."""

    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, *, position: Position, config: SearchConfig) -> None:
        super().__init__()
        self._position = position
        self._config = config

    def run(self) -> None:
        try:
            result: SearchResult = search_position(self._position, self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))