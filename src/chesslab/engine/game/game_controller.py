"""Thin orchestration layer for game flow and move logging."""


from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.game.game_record import GameRecord
from chesslab.engine.game.history import GameHistoryEntry
from chesslab.engine.game_status import is_checkmate, is_draw, is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves, is_legal_move
from chesslab.engine.make_unmake import make_move
from chesslab.engine.move import Move
from chesslab.engine.piece import Color, PieceType
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
        human_color: Color = Color.WHITE,
    ) -> None:
        self.position = position
        self.human_color = human_color
        self.record = GameRecord(
            event=event,
            site=site,
            date=datetime.now().strftime("%Y.%m.%d"),
            round=round_name,
            white=white_name if human_color is Color.WHITE else black_name,
            black=black_name if human_color is Color.WHITE else white_name,
            result="*",
            game_id=str(uuid4()),
        )

    @property
    def ply(self) -> int:
        return self.record.history.ply_count + 1

    @property
    def side_to_move(self) -> Color:
        return self.position.side_to_move

    def is_human_turn(self) -> bool:
        return self.position.side_to_move is self.human_color

    def is_game_over(self) -> bool:
        return self.record.result != "*"

    def legal_moves(self) -> list[Move]:
        return generate_legal_moves(self.position)

    def legal_moves_from(self, square: int) -> list[Move]:
        piece = self.position.piece_at(square)
        if piece is None:
            return []
        if piece.color is not self.position.side_to_move:
            return []
        return [move for move in generate_legal_moves(self.position) if move.from_sq == square]

    def requires_promotion_choice(self, from_sq: int, to_sq: int) -> bool:
        for move in self.legal_moves_from(from_sq):
            if move.to_sq == to_sq and move.promotion is not None:
                return True
        return False

    def find_legal_move(
        self,
        from_sq: int,
        to_sq: int,
        promotion: PieceType | None = None,
    ) -> Move | None:
        for move in self.legal_moves_from(from_sq):
            if move.to_sq != to_sq:
                continue
            if move.promotion != promotion and move.promotion is not None:
                continue
            if move.promotion is None and promotion is not None:
                continue
            return move
        return None

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

        make_move(self.position, move)

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

    def apply_engine_result(self, result: SearchResult) -> None:
        if result.best_move is None:
            self.record.result = self._current_result()
            return
        self.apply_move(result.best_move, search_result=result)

    def status_text(self) -> str:
        if is_checkmate(self.position):
            return "Checkmate"
        if is_stalemate(self.position):
            return "Stalemate"
        if is_draw(self.position):
            return "Draw"
        return "In progress"

    def _current_result(self) -> str:
        if is_checkmate(self.position):
            return "0-1" if self.position.side_to_move.value == "w" else "1-0"
        if is_stalemate(self.position) or is_draw(self.position):
            return "1/2-1/2"
        return "*"