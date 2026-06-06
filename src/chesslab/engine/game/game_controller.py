"""Thin orchestration layer for game flow and move logging."""


from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.game.game_record import GameRecord
from chesslab.engine.game.history import GameHistoryEntry
from chesslab.engine.game_status import is_checkmate, is_draw, is_stalemate
from chesslab.engine.legal_moves import is_legal_move
from chesslab.engine.make_unmake import make_move
from chesslab.engine.move import Move
from chesslab.engine.position import Position
from chesslab.engine.search.result import SearchResult
from chesslab.engine.search.stats import SearchStats
from chesslab.io.fen import to_fen
from chesslab.io.san import move_to_san


class GameController:
    """Owns a position and records applied moves with snapshots."""

    def __init__(
        self,
        position: Position,
        *,
        white_name: str = "Human",
        black_name: str = "Engine",
        event: str = "ChessLab Game",
        site: str = "Local",
        round_name: str = "1",
    ) -> None:
        self.position = position
        self.record = GameRecord(
            event=event,
            site=site,
            date=datetime.now().strftime("%Y.%m.%d"),
            round=round_name,
            white=white_name,
            black=black_name,
            result="*",
            game_id=str(uuid4()),
        )

    @property
    def ply(self) -> int:
        return self.record.history.ply_count + 1

    def apply_move(
        self,
        move: Move,
        *,
        search_result: SearchResult | None = None,
        san: str | None = None,
    ) -> None:
        if not is_legal_move(self.position, move):
            raise ValueError("Cannot apply illegal move")

        fen_before = to_fen(self.position)
        san_text = san or move_to_san(self.position, move)

        undo = make_move(self.position, move)
        _ = undo

        fen_after = to_fen(self.position)

        evaluation = (
            search_result.evaluation
            if search_result is not None
            else evaluate(self.position)
        )
        search_stats = (
            search_result.stats
            if search_result is not None
            else SearchStats(
                nodes=0,
                cutoffs=0,
                depth_reached=0,
                time_ms=0.0,
                principal_variation=[],
            )
        )

        self.record.history.append(
            GameHistoryEntry(
                ply=self.ply,
                move=move,
                fen_before=fen_before,
                fen_after=fen_after,
                evaluation=evaluation,
                search_stats=search_stats,
                san=san_text,
            )
        )
        self.record.result = self._current_result()

    def _current_result(self) -> str:
        if is_checkmate(self.position):
            return "0-1" if self.position.side_to_move.name == "WHITE" else "1-0"
        if is_stalemate(self.position) or is_draw(self.position):
            return "1/2-1/2"
        return "*"