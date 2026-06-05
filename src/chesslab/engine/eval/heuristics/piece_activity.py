"""Simple piece-activity evaluation."""


from __future__ import annotations

from chesslab.constants import (
    ADVANCED_BISHOP_BONUS,
    ADVANCED_KNIGHT_BONUS,
    DEVELOPED_MINOR_PIECE_BONUS,
    ROOK_OPEN_FILE_BONUS,
    ROOK_SEMIOPEN_FILE_BONUS,
)
from chesslab.engine.eval.features import file_of, pawn_squares
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position


def _starting_minor_rank(color: Color) -> int:
    return 0 if color is Color.WHITE else 7


def _pawn_files(position: Position, color: Color) -> set[int]:
    return {file_of(square) for square in pawn_squares(position, color)}


def _piece_activity_for_side(position: Position, color: Color) -> int:
    score = 0
    own_pawn_files = _pawn_files(position, color)
    enemy_pawn_files = _pawn_files(position, Color.BLACK if color is Color.WHITE else Color.WHITE)
    start_rank = _starting_minor_rank(color)

    for square, piece in enumerate(position.board):
        if piece is None or piece.color is not color:
            continue

        rank, file_index = position.rank_file_of(square)

        if piece.kind is PieceType.KNIGHT:
            if rank != start_rank:
                score += DEVELOPED_MINOR_PIECE_BONUS
            if (color is Color.WHITE and rank >= 3) or (color is Color.BLACK and rank <= 4):
                score += ADVANCED_KNIGHT_BONUS

        elif piece.kind is PieceType.BISHOP:
            if rank != start_rank:
                score += DEVELOPED_MINOR_PIECE_BONUS
            if (color is Color.WHITE and rank >= 3) or (color is Color.BLACK and rank <= 4):
                score += ADVANCED_BISHOP_BONUS

        elif piece.kind is PieceType.ROOK:
            own_has_pawn = file_index in own_pawn_files
            enemy_has_pawn = file_index in enemy_pawn_files
            if not own_has_pawn and not enemy_has_pawn:
                score += ROOK_OPEN_FILE_BONUS
            elif not own_has_pawn:
                score += ROOK_SEMIOPEN_FILE_BONUS

    return score


def piece_activity_balance(position: Position) -> int:
    """Return white-minus-black piece-activity balance."""
    return _piece_activity_for_side(position, Color.WHITE) - _piece_activity_for_side(position, Color.BLACK)