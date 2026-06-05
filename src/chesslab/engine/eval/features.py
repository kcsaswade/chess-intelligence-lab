"""Shared feature extraction helpers for evaluation heuristics."""


from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import index_to_rank_file
from chesslab.engine.king import require_king_square
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position

CENTER_SQUARES: tuple[int, int, int, int] = (27, 28, 35, 36)  # d4, e4, d5, e5


@dataclass(frozen=True)
class PieceSummary:
    pawns: int
    knights: int
    bishops: int
    rooks: int
    queens: int


def enemy_of(color: Color) -> Color:
    return Color.BLACK if color is Color.WHITE else Color.WHITE


def piece_counts(position: Position, color: Color) -> PieceSummary:
    counter: Counter[PieceType] = Counter()
    for piece in position.board:
        if piece is not None and piece.color is color:
            counter[piece.kind] += 1
    return PieceSummary(
        pawns=counter[PieceType.PAWN],
        knights=counter[PieceType.KNIGHT],
        bishops=counter[PieceType.BISHOP],
        rooks=counter[PieceType.ROOK],
        queens=counter[PieceType.QUEEN],
    )


def pawn_squares(position: Position, color: Color) -> list[int]:
    return [
        index
        for index, piece in enumerate(position.board)
        if piece is not None and piece.color is color and piece.kind is PieceType.PAWN
    ]


def non_pawn_piece_squares(position: Position, color: Color) -> list[tuple[int, PieceType]]:
    return [
        (index, piece.kind)
        for index, piece in enumerate(position.board)
        if piece is not None and piece.color is color and piece.kind is not PieceType.PAWN
    ]


def pawn_file_counts(position: Position, color: Color) -> list[int]:
    counts = [0] * 8
    for square in pawn_squares(position, color):
        _, file_index = index_to_rank_file(square)
        counts[file_index] += 1
    return counts


def king_square(position: Position, color: Color) -> int:
    return require_king_square(position, color)


def attacked_center_count(position: Position, color: Color) -> int:
    return sum(1 for square in CENTER_SQUARES if is_square_attacked(position, square, color))


def occupied_center_count(position: Position, color: Color) -> int:
    count = 0
    for square in CENTER_SQUARES:
        piece = position.piece_at(square)
        if piece is not None and piece.color is color:
            count += 1
    return count


def rank_of(square: int) -> int:
    rank, _ = index_to_rank_file(square)
    return rank


def file_of(square: int) -> int:
    _, file_index = index_to_rank_file(square)
    return file_index