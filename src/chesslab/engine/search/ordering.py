"""Deterministic move ordering helpers."""


from __future__ import annotations

from chesslab.engine.move import Move
from chesslab.engine.position import Position


def _ordering_key(move: Move) -> tuple[int, int, int, int, int]:
    promotion_rank = 0 if move.promotion is not None else 1
    capture_rank = 0 if move.is_capture or move.is_en_passant else 1
    castling_rank = 0 if move.is_castling else 1
    return (
        capture_rank,
        promotion_rank,
        castling_rank,
        move.from_sq,
        move.to_sq,
    )


def order_moves(position: Position, moves: list[Move]) -> list[Move]:
    """Return a deterministic move ordering for search."""
    del position
    return sorted(moves, key=_ordering_key)