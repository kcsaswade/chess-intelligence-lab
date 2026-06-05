"""Mobility evaluation using legal move counts."""


from __future__ import annotations

from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.move import Move
from chesslab.engine.piece import Color
from chesslab.engine.position import Position


def _legal_move_count_for_side(position: Position, color: Color) -> int:
    if position.side_to_move is color:
        return len(generate_legal_moves(position))

    null_switch = Move(from_sq=0, to_sq=0)
    original_side = position.side_to_move
    position.side_to_move = color
    try:
        return len(generate_legal_moves(position))
    finally:
        position.side_to_move = original_side


def mobility_balance(position: Position) -> int:
    """Return white-minus-black mobility balance."""
    white_moves = _legal_move_count_for_side(position, Color.WHITE)
    black_moves = _legal_move_count_for_side(position, Color.BLACK)
    return white_moves - black_moves