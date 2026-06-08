"""Main application window for the playable GUI."""


from __future__ import annotations


from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QWidget,
)

from chesslab.constants import (
    APP_WINDOW_TITLE,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    GUI_SIDE_PANEL_MIN_WIDTH,
)
from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game.game_controller import GameController
from chesslab.engine.move import Move
from chesslab.engine.piece import Color
from chesslab.engine.position import Position
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.result import SearchResult
from chesslab.engine.search.stats import SearchStats
from chesslab.engine.startpos import STARTPOS_FEN
from chesslab.gui.board_widget import BoardWidget
from chesslab.gui.promotion_dialog import PromotionDialog
from chesslab.gui.side_panel import SidePanel
from chesslab.gui.viewmodels import (
    build_evaluation_lines,
    build_game_info_model,
    build_search_stats_model,
)
from chesslab.gui.workers import SearchWorker


class MainWindow(QMainWindow):
    """Top-level composition and signal wiring for the GUI."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_WINDOW_TITLE)
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

        self.controller = GameController(
            Position.from_fen(STARTPOS_FEN),
            human_color=Color.WHITE,
        )
        self.search_config = SearchConfig(depth=3)

        self._engine_thread: QThread | None = None
        self._engine_worker: SearchWorker | None = None
        self._search_in_flight = False
        self._latest_search_result: SearchResult | None = None

        self.board_widget = BoardWidget()
        self.side_panel = SidePanel()
        self.side_panel.setMinimumWidth(GUI_SIDE_PANEL_MIN_WIDTH)

        self._build_ui()
        self._connect_signals()
        self._refresh_all()

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        layout.addWidget(self.board_widget, stretch=3)
        layout.addWidget(self.side_panel, stretch=2)
        self.setCentralWidget(container)

    def _connect_signals(self) -> None:
        self.board_widget.move_requested.connect(self.on_human_move_requested)

    def _refresh_all(self, latest_result: SearchResult | None = None, thinking: bool = False) -> None:
        if latest_result is not None:
            self._latest_search_result = latest_result

        last_move = (
            self.controller.record.history.entries[-1].move
            if self.controller.record.history.entries
            else None
        )
        self.board_widget.set_position(self.controller.position, last_move=last_move)

        self.side_panel.game_info_widget.update_model(
            build_game_info_model(
                controller=self.controller,
                thinking=thinking,
            )
        )

        evaluation = self._current_evaluation()
        self.side_panel.eval_panel.set_lines(build_evaluation_lines(evaluation))
        self.side_panel.search_stats_panel.update_model(
            build_search_stats_model(self._current_stats())
        )
        self.side_panel.move_list_widget.set_moves(
            [entry.san or "" for entry in self.controller.record.history.entries]
        )

    def _current_evaluation(self) -> EvaluationResult:
        if self._latest_search_result is not None:
            return self._latest_search_result.evaluation
        return evaluate(self.controller.position)

    def _current_stats(self) -> SearchStats:
        if self._latest_search_result is not None:
            return self._latest_search_result.stats
        return SearchStats(
            nodes=0,
            cutoffs=0,
            depth_reached=0,
            time_ms=0.0,
            principal_variation=[],
        )

    def on_human_move_requested(self, move: Move) -> None:
        if self._search_in_flight:
            return
        if not self.controller.is_human_turn():
            return

        try:
            move_to_apply = move
            if move.promotion is None and self.controller.requires_promotion_choice(move.from_sq, move.to_sq):
                promotion = PromotionDialog.choose_promotion(self)
                if promotion is None:
                    self.board_widget.clear_selection()
                    return
                resolved_move = self.controller.find_legal_move(move.from_sq, move.to_sq, promotion)
                if resolved_move is None:
                    raise ValueError("Promotion move could not be resolved")
                move_to_apply = resolved_move

            self._latest_search_result = None
            self.controller.apply_move(move_to_apply)
            self._refresh_all()

            if self.controller.is_game_over():
                self._show_game_over()
                return

            self._start_engine_search()
        except Exception as exc:
            QMessageBox.critical(self, "Move Error", str(exc))
            self.board_widget.clear_selection()
            self._refresh_all()

    def _start_engine_search(self) -> None:
        if self._engine_thread is not None:
            return

        self._search_in_flight = True
        self.board_widget.set_enabled_for_human(False)
        self._refresh_all(thinking=True)

        self._engine_thread = QThread(self)
        self._engine_worker = SearchWorker(
            position=self.controller.position.copy_shallow(),
            config=self.search_config,
        )
        self._engine_worker.moveToThread(self._engine_thread)

        self._engine_thread.started.connect(self._engine_worker.run)
        self._engine_worker.finished.connect(self.on_engine_search_finished)
        self._engine_worker.failed.connect(self.on_engine_search_failed)
        self._engine_worker.finished.connect(self._engine_thread.quit)
        self._engine_worker.failed.connect(self._engine_thread.quit)
        self._engine_thread.finished.connect(self._cleanup_engine_thread)

        self._engine_thread.start()

    def _cleanup_engine_thread(self) -> None:
        if self._engine_worker is not None:
            self._engine_worker.deleteLater()
            self._engine_worker = None
        if self._engine_thread is not None:
            self._engine_thread.deleteLater()
            self._engine_thread = None

    def on_engine_search_finished(self, result: object) -> None:
        self._search_in_flight = False
        self.board_widget.set_enabled_for_human(True)

        if not isinstance(result, SearchResult):
            self.on_engine_search_failed("Engine returned an invalid search result.")
            return

        try:
            self._latest_search_result = result
            self.controller.apply_engine_result(result)
            self._refresh_all(latest_result=result)
            if self.controller.is_game_over():
                self._show_game_over()
        except Exception as exc:
            QMessageBox.critical(self, "Engine Error", str(exc))
            self._refresh_all(latest_result=result)

    def on_engine_search_failed(self, message: str) -> None:
        self._search_in_flight = False
        self.board_widget.set_enabled_for_human(True)
        QMessageBox.critical(self, "Search Error", message)
        self._refresh_all()

    def _show_game_over(self) -> None:
        QMessageBox.information(
            self,
            "Game Over",
            f"{self.controller.status_text()}\nResult: {self.controller.record.result}",
        )