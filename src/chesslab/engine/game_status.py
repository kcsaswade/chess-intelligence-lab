"""Game-status helpers based on legal moves, check state, and draw state."""

from __future__ import annotations

from chesslab.constants import HALFMOVE_CLOCK_DRAW_THRESHOLD
from chesslab.engine.attacks import is_in_check
from chesslab.engine.history import PositionHistory
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


def is_draw_by_fifty_move_rule(position: Position) -> bool:
    """Return whether the position is drawable by the fifty-move rule."""
    return position.halfmove_clock >= HALFMOVE_CLOCK_DRAW_THRESHOLD


def is_draw_by_repetition(position: Position, history: PositionHistory) -> bool:
    """Return whether the current position has occurred at least three times."""
    return history.count_current(position) >= 3


def is_draw(position: Position, history: PositionHistory | None = None) -> bool:
    """Return whether any currently supported draw condition applies."""
    if is_stalemate(position):
        return True
    if is_draw_by_fifty_move_rule(position):
        return True
    if history is not None and is_draw_by_repetition(position, history):
        return True
    return False