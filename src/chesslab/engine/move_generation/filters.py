"""Light board-state filters for move generation."""

from chesslab.engine.piece import Color
from chesslab.engine.position import Position


def is_empty(position: Position, square: int) -> bool:
    """Return whether a square is empty."""
    return position.piece_at(square) is None


def is_own_piece(position: Position, square: int, color: Color) -> bool:
    """Return whether a square contains a piece of the given color."""
    piece = position.piece_at(square)
    return piece is not None and piece.color is color


def is_enemy_piece(position: Position, square: int, color: Color) -> bool:
    """Return whether a square contains an opposing piece."""
    piece = position.piece_at(square)
    return piece is not None and piece.color is not color