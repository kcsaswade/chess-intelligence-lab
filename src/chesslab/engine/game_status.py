"""Game-status helpers based on legal moves and check state."""

from __future__ import annotations

from chesslab.engine.attacks import is_in_check
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.position import Position


def has_any_legal_moves(position: Position) -> bool:
    """Return whether the side to move has at least one legal move."""
    return bool(generate_legal_moves(position))


def is_checkmate(position: Position) -> bool:
    """Return whether the side to move is checkmated."""
    return is_in_check(position, position.side_to_move) and not has_any_legal_moves(position)


def is_stalemate(position: Position) -> bool:
    """Return whether the side to move is stalemated."""
    return not is_in_check(position, position.side_to_move) and not has_any_legal_moves(position)