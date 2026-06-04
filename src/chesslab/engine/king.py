"""Helpers for locating kings in a position."""

from __future__ import annotations

from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position
from chesslab.errors import InvalidMoveError


def find_king_square(position: Position, color: Color) -> int | None:
    """Return the square index of the king for the given color, if present."""
    for square, piece in enumerate(position.board):
        if piece is not None and piece.color is color and piece.kind is PieceType.KING:
            return square
    return None


def require_king_square(position: Position, color: Color) -> int:
    """Return the king square or raise if the king is absent."""
    square = find_king_square(position, color)
    if square is None:
        raise InvalidMoveError(f"No king found for {color.name}")
    return square