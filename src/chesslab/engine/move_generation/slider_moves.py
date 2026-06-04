"""Slider pseudo-legal move generation for rook, bishop, and queen."""

from __future__ import annotations

from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.move import Move
from chesslab.engine.move_generation.filters import (
    is_empty,
    is_enemy_piece,
    is_own_piece,
)
from chesslab.engine.move_generation.rays import (
    BISHOP_DIRECTIONS,
    QUEEN_DIRECTIONS,
    ROOK_DIRECTIONS,
)
from chesslab.engine.piece import PieceType
from chesslab.engine.position import Position
from chesslab.types import Direction


def _generate_slider_moves(
    position: Position,
    from_sq: int,
    directions: tuple[Direction, ...],
) -> list[Move]:
    piece = position.piece_at(from_sq)
    if piece is None:
        return []

    start_rank, start_file = position.rank_file_of(from_sq)
    moves: list[Move] = []

    for rank_delta, file_delta in directions:
        rank = start_rank + rank_delta
        file = start_file + file_delta

        while is_valid_rank_file(rank, file):
            to_sq = rank_file_to_index(rank, file)

            if is_own_piece(position, to_sq, piece.color):
                break

            if is_empty(position, to_sq):
                moves.append(Move(from_sq=from_sq, to_sq=to_sq))
            else:
                if is_enemy_piece(position, to_sq, piece.color):
                    moves.append(Move(from_sq=from_sq, to_sq=to_sq, is_capture=True))
                break

            rank += rank_delta
            file += file_delta

    return moves


def generate_rook_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate pseudo-legal rook moves from a square."""
    return _generate_slider_moves(position, from_sq, ROOK_DIRECTIONS)


def generate_bishop_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate pseudo-legal bishop moves from a square."""
    return _generate_slider_moves(position, from_sq, BISHOP_DIRECTIONS)


def generate_queen_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate pseudo-legal queen moves from a square."""
    return _generate_slider_moves(position, from_sq, QUEEN_DIRECTIONS)


def generate_slider_moves(position: Position, from_sq: int) -> list[Move]:
    """Dispatch slider moves based on the piece on the square."""
    piece = position.piece_at(from_sq)
    if piece is None:
        return []

    if piece.kind is PieceType.ROOK:
        return generate_rook_moves(position, from_sq)
    if piece.kind is PieceType.BISHOP:
        return generate_bishop_moves(position, from_sq)
    if piece.kind is PieceType.QUEEN:
        return generate_queen_moves(position, from_sq)
    return []