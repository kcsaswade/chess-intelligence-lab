"""Directional helpers for slider move generation."""

from chesslab.types import Direction

ROOK_DIRECTIONS: tuple[Direction, ...] = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
)

BISHOP_DIRECTIONS: tuple[Direction, ...] = (
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)

QUEEN_DIRECTIONS: tuple[Direction, ...] = ROOK_DIRECTIONS + BISHOP_DIRECTIONS