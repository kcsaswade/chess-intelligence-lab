"""In-place make/unmake support for legal and pseudo-legal moves."""

from __future__ import annotations

from chesslab.constants import (
    BLACK_KINGSIDE_CASTLE_KING_TO,
    BLACK_KINGSIDE_CASTLE_ROOK_FROM,
    BLACK_KINGSIDE_CASTLE_ROOK_TO,
    BLACK_QUEENSIDE_CASTLE_KING_TO,
    BLACK_QUEENSIDE_CASTLE_ROOK_FROM,
    BLACK_QUEENSIDE_CASTLE_ROOK_TO,
    WHITE_KINGSIDE_CASTLE_KING_TO,
    WHITE_KINGSIDE_CASTLE_ROOK_FROM,
    WHITE_KINGSIDE_CASTLE_ROOK_TO,
    WHITE_QUEENSIDE_CASTLE_KING_TO,
    WHITE_QUEENSIDE_CASTLE_ROOK_FROM,
    WHITE_QUEENSIDE_CASTLE_ROOK_TO,
)
from chesslab.engine.board import rank_file_to_index
from chesslab.engine.castling import CastlingRights
from chesslab.engine.move import Move
from chesslab.engine.move_state import MoveUndoInfo
from chesslab.engine.piece import Color, Piece, PieceType
from chesslab.engine.position import Position
from chesslab.engine.validators import (
    assert_move_on_board,
    assert_piece_belongs_to_side_to_move,
    assert_piece_exists_at_source,
)


def _copy_castling_rights(position: Position) -> CastlingRights:
    return CastlingRights(
        white_kingside=position.castling_rights.white_kingside,
        white_queenside=position.castling_rights.white_queenside,
        black_kingside=position.castling_rights.black_kingside,
        black_queenside=position.castling_rights.black_queenside,
    )


def _enemy_of(color: Color) -> Color:
    return Color.BLACK if color is Color.WHITE else Color.WHITE


def _update_castling_rights_for_move(position: Position, move: Move, moved_piece: Piece) -> None:
    if moved_piece.kind is PieceType.KING:
        if moved_piece.color is Color.WHITE:
            position.castling_rights.white_kingside = False
            position.castling_rights.white_queenside = False
        else:
            position.castling_rights.black_kingside = False
            position.castling_rights.black_queenside = False

    if moved_piece.kind is PieceType.ROOK:
        if moved_piece.color is Color.WHITE:
            if move.from_sq == 0:
                position.castling_rights.white_queenside = False
            elif move.from_sq == 7:
                position.castling_rights.white_kingside = False
        else:
            if move.from_sq == 56:
                position.castling_rights.black_queenside = False
            elif move.from_sq == 63:
                position.castling_rights.black_kingside = False


def _update_castling_rights_for_captured_rook(
    position: Position,
    move: Move,
    captured_piece: Piece | None,
) -> None:
    if captured_piece is None or captured_piece.kind is not PieceType.ROOK:
        return

    if captured_piece.color is Color.WHITE:
        if move.to_sq == 0:
            position.castling_rights.white_queenside = False
        elif move.to_sq == 7:
            position.castling_rights.white_kingside = False
    else:
        if move.to_sq == 56:
            position.castling_rights.black_queenside = False
        elif move.to_sq == 63:
            position.castling_rights.black_kingside = False


def _en_passant_target_for_double_push(
    position: Position,
    move: Move,
    moved_piece: Piece,
) -> int | None:
    if moved_piece.kind is not PieceType.PAWN or not move.is_double_pawn_push:
        return None

    from_rank, from_file = position.rank_file_of(move.from_sq)
    to_rank, _ = position.rank_file_of(move.to_sq)
    middle_rank = (from_rank + to_rank) // 2
    return rank_file_to_index(middle_rank, from_file)


def _castling_rook_squares(move: Move, moved_piece: Piece) -> tuple[int, int] | None:
    if not move.is_castling or moved_piece.kind is not PieceType.KING:
        return None

    if moved_piece.color is Color.WHITE:
        if move.to_sq == WHITE_KINGSIDE_CASTLE_KING_TO:
            return (WHITE_KINGSIDE_CASTLE_ROOK_FROM, WHITE_KINGSIDE_CASTLE_ROOK_TO)
        if move.to_sq == WHITE_QUEENSIDE_CASTLE_KING_TO:
            return (WHITE_QUEENSIDE_CASTLE_ROOK_FROM, WHITE_QUEENSIDE_CASTLE_ROOK_TO)
    else:
        if move.to_sq == BLACK_KINGSIDE_CASTLE_KING_TO:
            return (BLACK_KINGSIDE_CASTLE_ROOK_FROM, BLACK_KINGSIDE_CASTLE_ROOK_TO)
        if move.to_sq == BLACK_QUEENSIDE_CASTLE_KING_TO:
            return (BLACK_QUEENSIDE_CASTLE_ROOK_FROM, BLACK_QUEENSIDE_CASTLE_ROOK_TO)

    return None


def _en_passant_captured_square(position: Position, move: Move, moved_piece: Piece) -> int | None:
    if not move.is_en_passant or moved_piece.kind is not PieceType.PAWN:
        return None

    from_rank, to_file = position.rank_file_of(move.from_sq)[0], position.rank_file_of(move.to_sq)[1]
    return rank_file_to_index(from_rank, to_file)


def make_move(position: Position, move: Move) -> MoveUndoInfo:
    """Apply a move in place and return undo information."""
    assert_move_on_board(move)
    assert_piece_exists_at_source(position, move)
    assert_piece_belongs_to_side_to_move(position, move)

    moved_piece = position.piece_at(move.from_sq)
    assert moved_piece is not None

    captured_piece = position.piece_at(move.to_sq)
    en_passant_capture_square = _en_passant_captured_square(position, move, moved_piece)
    if move.is_en_passant and en_passant_capture_square is not None:
        captured_piece = position.piece_at(en_passant_capture_square)

    rook_squares = _castling_rook_squares(move, moved_piece)
    undo = MoveUndoInfo(
        moved_piece=moved_piece,
        captured_piece=captured_piece,
        previous_castling_rights=_copy_castling_rights(position),
        previous_en_passant_square=position.en_passant_square,
        previous_halfmove_clock=position.halfmove_clock,
        previous_fullmove_number=position.fullmove_number,
        previous_side_to_move=position.side_to_move,
        en_passant_captured_square=en_passant_capture_square,
        castling_rook_from=rook_squares[0] if rook_squares is not None else None,
        castling_rook_to=rook_squares[1] if rook_squares is not None else None,
    )

    _update_castling_rights_for_move(position, move, moved_piece)
    _update_castling_rights_for_captured_rook(position, move, captured_piece)

    position.remove_piece(move.from_sq)

    if move.is_en_passant and en_passant_capture_square is not None:
        position.remove_piece(en_passant_capture_square)

    placed_piece = moved_piece
    if move.promotion is not None:
        placed_piece = Piece(color=moved_piece.color, kind=move.promotion)

    position.set_piece(move.to_sq, placed_piece)

    if rook_squares is not None:
        rook_from, rook_to = rook_squares
        rook_piece = position.remove_piece(rook_from)
        assert rook_piece is not None
        position.set_piece(rook_to, rook_piece)

    if moved_piece.kind is PieceType.PAWN or captured_piece is not None:
        position.halfmove_clock = 0
    else:
        position.halfmove_clock += 1

    position.en_passant_square = _en_passant_target_for_double_push(position, move, moved_piece)

    if undo.previous_side_to_move is Color.BLACK:
        position.fullmove_number += 1

    position.side_to_move = _enemy_of(undo.previous_side_to_move)
    position.validate_basic_integrity()
    return undo


def unmake_move(position: Position, move: Move, undo: MoveUndoInfo) -> None:
    """Restore the exact previous position from undo information."""
    assert_move_on_board(move)

    if undo.castling_rook_from is not None and undo.castling_rook_to is not None:
        rook_piece = position.remove_piece(undo.castling_rook_to)
        assert rook_piece is not None
        position.set_piece(undo.castling_rook_from, rook_piece)

    position.remove_piece(move.to_sq)
    position.set_piece(move.from_sq, undo.moved_piece)

    if move.is_en_passant and undo.en_passant_captured_square is not None:
        position.set_piece(undo.en_passant_captured_square, undo.captured_piece)
    else:
        position.set_piece(move.to_sq, undo.captured_piece)

    position.castling_rights = undo.previous_castling_rights
    position.en_passant_square = undo.previous_en_passant_square
    position.halfmove_clock = undo.previous_halfmove_clock
    position.fullmove_number = undo.previous_fullmove_number
    position.side_to_move = undo.previous_side_to_move
    position.validate_basic_integrity()