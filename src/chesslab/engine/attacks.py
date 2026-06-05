"""Attack detection helpers."""

from __future__ import annotations

from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.king import require_king_square
from chesslab.engine.move_generation.king_moves import KING_OFFSETS
from chesslab.engine.move_generation.knight_moves import KNIGHT_OFFSETS
from chesslab.engine.move_generation.rays import BISHOP_DIRECTIONS, ROOK_DIRECTIONS
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position


def _pawn_attacks_square(position: Position, square: int, by_color: Color) -> list[int]:
    target_rank, target_file = position.rank_file_of(square)
    attackers: list[int] = []

    candidate_offsets = ((-1, -1), (-1, 1)) if by_color is Color.WHITE else ((1, -1), (1, 1))

    for rank_delta, file_delta in candidate_offsets:
        rank = target_rank + rank_delta
        file = target_file + file_delta
        if not is_valid_rank_file(rank, file):
            continue

        from_sq = rank_file_to_index(rank, file)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.PAWN:
            attackers.append(from_sq)

    return attackers


def _knight_attacks_square(position: Position, square: int, by_color: Color) -> list[int]:
    target_rank, target_file = position.rank_file_of(square)
    attackers: list[int] = []

    for rank_delta, file_delta in KNIGHT_OFFSETS:
        rank = target_rank + rank_delta
        file = target_file + file_delta
        if not is_valid_rank_file(rank, file):
            continue

        from_sq = rank_file_to_index(rank, file)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.KNIGHT:
            attackers.append(from_sq)

    return attackers


def _king_attacks_square(position: Position, square: int, by_color: Color) -> list[int]:
    target_rank, target_file = position.rank_file_of(square)
    attackers: list[int] = []

    for rank_delta, file_delta in KING_OFFSETS:
        rank = target_rank + rank_delta
        file = target_file + file_delta
        if not is_valid_rank_file(rank, file):
            continue

        from_sq = rank_file_to_index(rank, file)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.KING:
            attackers.append(from_sq)

    return attackers


def _scan_slider_attackers(
    position: Position,
    square: int,
    by_color: Color,
    directions: tuple[tuple[int, int], ...],
    valid_kinds: set[PieceType],
) -> list[int]:
    target_rank, target_file = position.rank_file_of(square)
    attackers: list[int] = []

    for rank_delta, file_delta in directions:
        rank = target_rank + rank_delta
        file = target_file + file_delta

        while is_valid_rank_file(rank, file):
            from_sq = rank_file_to_index(rank, file)
            piece = position.piece_at(from_sq)

            if piece is None:
                rank += rank_delta
                file += file_delta
                continue

            if piece.color is by_color and piece.kind in valid_kinds:
                attackers.append(from_sq)
            break

    return attackers


def _slider_attacks_square(position: Position, square: int, by_color: Color) -> list[int]:
    attackers: list[int] = []
    attackers.extend(
        _scan_slider_attackers(
            position,
            square,
            by_color,
            ROOK_DIRECTIONS,
            {PieceType.ROOK, PieceType.QUEEN},
        )
    )
    attackers.extend(
        _scan_slider_attackers(
            position,
            square,
            by_color,
            BISHOP_DIRECTIONS,
            {PieceType.BISHOP, PieceType.QUEEN},
        )
    )
    return attackers


def attackers_to_square(position: Position, square: int, by_color: Color) -> list[int]:
    """Return squares of pieces of by_color attacking the target square."""
    attackers: list[int] = []
    attackers.extend(_pawn_attacks_square(position, square, by_color))
    attackers.extend(_knight_attacks_square(position, square, by_color))
    attackers.extend(_king_attacks_square(position, square, by_color))
    attackers.extend(_slider_attacks_square(position, square, by_color))
    return attackers


def is_square_attacked(position: Position, square: int, by_color: Color) -> bool:
    """Return whether a square is attacked by the given color."""
    return bool(attackers_to_square(position, square, by_color))


def is_in_check(position: Position, color: Color) -> bool:
    """Return whether the given color's king is currently attacked."""
    king_square = require_king_square(position, color)
    enemy_color = Color.BLACK if color is Color.WHITE else Color.WHITE
    return is_square_attacked(position, king_square, enemy_color)