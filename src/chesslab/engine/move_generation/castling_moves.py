"""Pseudo-legal castling generation with explicit castling constraints."""

from __future__ import annotations

from chesslab.constants import (
    BLACK_KINGSIDE_CASTLE_KING_FROM,
    BLACK_KINGSIDE_CASTLE_KING_TO,
    BLACK_KINGSIDE_CASTLE_ROOK_FROM,
    BLACK_QUEENSIDE_CASTLE_KING_TO,
    BLACK_QUEENSIDE_CASTLE_ROOK_FROM,
    WHITE_KINGSIDE_CASTLE_KING_FROM,
    WHITE_KINGSIDE_CASTLE_KING_TO,
    WHITE_KINGSIDE_CASTLE_ROOK_FROM,
    WHITE_QUEENSIDE_CASTLE_KING_TO,
    WHITE_QUEENSIDE_CASTLE_ROOK_FROM,
)
from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.move import Move
from chesslab.engine.move_generation.rays import BISHOP_DIRECTIONS, ROOK_DIRECTIONS
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position


def _enemy_of(color: Color) -> Color:
    return Color.BLACK if color is Color.WHITE else Color.WHITE


def _path_is_empty(position: Position, squares: tuple[int, ...]) -> bool:
    return all(position.piece_at(square) is None for square in squares)


def _square_attacked_by_knight(position: Position, square: int, by_color: Color) -> bool:
    target_rank, target_file = position.rank_file_of(square)
    knight_offsets = (
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    )
    for dr, df in knight_offsets:
        r = target_rank + dr
        f = target_file + df
        if not is_valid_rank_file(r, f):
            continue
        from_sq = rank_file_to_index(r, f)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.KNIGHT:
            return True
    return False


def _square_attacked_by_pawn(position: Position, square: int, by_color: Color) -> bool:
    target_rank, target_file = position.rank_file_of(square)
    if by_color is Color.WHITE:
        candidates = ((-1, -1), (-1, 1))
    else:
        candidates = ((1, -1), (1, 1))

    for dr, df in candidates:
        r = target_rank + dr
        f = target_file + df
        if not is_valid_rank_file(r, f):
            continue
        from_sq = rank_file_to_index(r, f)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.PAWN:
            return True
    return False


def _square_attacked_by_king(position: Position, square: int, by_color: Color) -> bool:
    target_rank, target_file = position.rank_file_of(square)
    king_offsets = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )
    for dr, df in king_offsets:
        r = target_rank + dr
        f = target_file + df
        if not is_valid_rank_file(r, f):
            continue
        from_sq = rank_file_to_index(r, f)
        piece = position.piece_at(from_sq)
        if piece is not None and piece.color is by_color and piece.kind is PieceType.KING:
            return True
    return False


def _square_attacked_by_sliders(position: Position, square: int, by_color: Color) -> bool:
    target_rank, target_file = position.rank_file_of(square)

    for dr, df in ROOK_DIRECTIONS:
        r = target_rank + dr
        f = target_file + df
        while is_valid_rank_file(r, f):
            from_sq = rank_file_to_index(r, f)
            piece = position.piece_at(from_sq)
            if piece is None:
                r += dr
                f += df
                continue
            if piece.color is by_color and piece.kind in {PieceType.ROOK, PieceType.QUEEN}:
                return True
            break

    for dr, df in BISHOP_DIRECTIONS:
        r = target_rank + dr
        f = target_file + df
        while is_valid_rank_file(r, f):
            from_sq = rank_file_to_index(r, f)
            piece = position.piece_at(from_sq)
            if piece is None:
                r += dr
                f += df
                continue
            if piece.color is by_color and piece.kind in {PieceType.BISHOP, PieceType.QUEEN}:
                return True
            break

    return False


def _square_attacked(position: Position, square: int, by_color: Color) -> bool:
    """Local attack test to avoid circular import with attacks.py."""
    return (
        _square_attacked_by_knight(position, square, by_color)
        or _square_attacked_by_pawn(position, square, by_color)
        or _square_attacked_by_king(position, square, by_color)
        or _square_attacked_by_sliders(position, square, by_color)
    )


def _squares_not_attacked(position: Position, squares: tuple[int, ...], enemy: Color) -> bool:
    return all(not _square_attacked(position, sq, enemy) for sq in squares)


def generate_castling_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate castling moves for a king square when explicitly legal."""
    piece = position.piece_at(from_sq)
    if piece is None or piece.kind is not PieceType.KING or piece.color is not position.side_to_move:
        return []

    enemy = _enemy_of(piece.color)
    moves: list[Move] = []

    if piece.color is Color.WHITE and from_sq == WHITE_KINGSIDE_CASTLE_KING_FROM:
        kingside_rook = position.piece_at(WHITE_KINGSIDE_CASTLE_ROOK_FROM)
        if (
            position.castling_rights.white_kingside
            and kingside_rook is not None
            and kingside_rook.kind is PieceType.ROOK
            and kingside_rook.color is Color.WHITE
            and _path_is_empty(position, (5, 6))
            and _squares_not_attacked(position, (4, 5, 6), enemy)
        ):
            moves.append(Move(from_sq=from_sq, to_sq=WHITE_KINGSIDE_CASTLE_KING_TO, is_castling=True))

        queenside_rook = position.piece_at(WHITE_QUEENSIDE_CASTLE_ROOK_FROM)
        if (
            position.castling_rights.white_queenside
            and queenside_rook is not None
            and queenside_rook.kind is PieceType.ROOK
            and queenside_rook.color is Color.WHITE
            and _path_is_empty(position, (1, 2, 3))
            and _squares_not_attacked(position, (4, 3, 2), enemy)
        ):
            moves.append(Move(from_sq=from_sq, to_sq=WHITE_QUEENSIDE_CASTLE_KING_TO, is_castling=True))

    elif piece.color is Color.BLACK and from_sq == BLACK_KINGSIDE_CASTLE_KING_FROM:
        kingside_rook = position.piece_at(BLACK_KINGSIDE_CASTLE_ROOK_FROM)
        if (
            position.castling_rights.black_kingside
            and kingside_rook is not None
            and kingside_rook.kind is PieceType.ROOK
            and kingside_rook.color is Color.BLACK
            and _path_is_empty(position, (61, 62))
            and _squares_not_attacked(position, (60, 61, 62), enemy)
        ):
            moves.append(Move(from_sq=from_sq, to_sq=BLACK_KINGSIDE_CASTLE_KING_TO, is_castling=True))

        queenside_rook = position.piece_at(BLACK_QUEENSIDE_CASTLE_ROOK_FROM)
        if (
            position.castling_rights.black_queenside
            and queenside_rook is not None
            and queenside_rook.kind is PieceType.ROOK
            and queenside_rook.color is Color.BLACK
            and _path_is_empty(position, (57, 58, 59))
            and _squares_not_attacked(position, (60, 59, 58), enemy)
        ):
            moves.append(Move(from_sq=from_sq, to_sq=BLACK_QUEENSIDE_CASTLE_KING_TO, is_castling=True))

    return moves