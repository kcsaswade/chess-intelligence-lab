"""King pseudo-legal move generation."""

from __future__ import annotations

from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.move import Move
from chesslab.engine.move_generation.filters import is_enemy_piece, is_own_piece
from chesslab.engine.position import Position

KING_OFFSETS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)


def generate_king_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate pseudo-legal king moves from a square."""
    piece = position.piece_at(from_sq)
    if piece is None:
        return []

    rank, file = position.rank_file_of(from_sq)
    moves: list[Move] = []

    for rank_delta, file_delta in KING_OFFSETS:
        target_rank = rank + rank_delta
        target_file = file + file_delta

        if not is_valid_rank_file(target_rank, target_file):
            continue

        to_sq = rank_file_to_index(target_rank, target_file)
        if is_own_piece(position, to_sq, piece.color):
            continue

        moves.append(
            Move(
                from_sq=from_sq,
                to_sq=to_sq,
                is_capture=is_enemy_piece(position, to_sq, piece.color),
            )
        )

    return moves