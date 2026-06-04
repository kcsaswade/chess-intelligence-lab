"""Helpers for interpreting move flags."""

from chesslab.engine.move import Move


def is_promotion(move: Move) -> bool:
    """Return whether the move is a promotion."""
    return move.promotion is not None


def is_special_move(move: Move) -> bool:
    """Return whether the move uses any non-basic move flag."""
    return (
        move.is_castling
        or move.is_en_passant
        or move.is_double_pawn_push
        or move.promotion is not None
    )