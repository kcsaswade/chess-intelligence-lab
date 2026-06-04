"""Legal move generation built on pseudo-legal generation plus self-check filtering."""

from __future__ import annotations

from chesslab.engine.attacks import is_in_check
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.move_generation.generator import generate_pseudolegal_moves
from chesslab.engine.position import Position


def is_legal_move(position: Position, move: Move) -> bool:
    """Return whether a pseudo-legal move is legal with respect to king safety."""
    moving_color = position.side_to_move
    undo = make_move(position, move)
    try:
        return not is_in_check(position, moving_color)
    finally:
        unmake_move(position, move, undo)


def generate_legal_moves(position: Position) -> list[Move]:
    """Generate legal moves by filtering pseudo-legal moves."""
    legal_moves: list[Move] = []
    for move in generate_pseudolegal_moves(position):
        if is_legal_move(position, move):
            legal_moves.append(move)
    return legal_moves