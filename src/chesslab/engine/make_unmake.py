"""In-place make/unmake support for pseudo-legal moves."""

from __future__ import annotations

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


def make_move(position: Position, move: Move) -> MoveUndoInfo:
    """Apply a pseudo-legal move in place and return undo information."""
    assert_move_on_board(move)
    assert_piece_exists_at_source(position, move)
    assert_piece_belongs_to_side_to_move(position, move)

    moved_piece = position.piece_at(move.from_sq)
    assert moved_piece is not None

    captured_piece = position.piece_at(move.to_sq)
    undo = MoveUndoInfo(
        moved_piece=moved_piece,
        captured_piece=captured_piece,
        previous_castling_rights=_copy_castling_rights(position),
        previous_en_passant_square=position.en_passant_square,
        previous_halfmove_clock=position.halfmove_clock,
        previous_fullmove_number=position.fullmove_number,
        previous_side_to_move=position.side_to_move,
    )

    _update_castling_rights_for_move(position, move, moved_piece)
    _update_castling_rights_for_captured_rook(position, move, captured_piece)

    position.remove_piece(move.from_sq)

    placed_piece = moved_piece
    if move.promotion is not None:
        placed_piece = Piece(color=moved_piece.color, kind=move.promotion)

    position.set_piece(move.to_sq, placed_piece)

    if moved_piece.kind is PieceType.PAWN or captured_piece is not None:
        position.halfmove_clock = 0
    else:
        position.halfmove_clock += 1

    position.en_passant_square = _en_passant_target_for_double_push(position, move, moved_piece)

    if undo.previous_side_to_move is Color.BLACK:
        position.fullmove_number += 1

    position.side_to_move = (
        Color.BLACK if undo.previous_side_to_move is Color.WHITE else Color.WHITE
    )
    position.validate_basic_integrity()
    return undo


def unmake_move(position: Position, move: Move, undo: MoveUndoInfo) -> None:
    """Restore the exact previous position from undo information."""
    assert_move_on_board(move)

    position.remove_piece(move.to_sq)
    position.set_piece(move.from_sq, undo.moved_piece)
    position.set_piece(move.to_sq, undo.captured_piece)

    position.castling_rights = undo.previous_castling_rights
    position.en_passant_square = undo.previous_en_passant_square
    position.halfmove_clock = undo.previous_halfmove_clock
    position.fullmove_number = undo.previous_fullmove_number
    position.side_to_move = undo.previous_side_to_move
    position.validate_basic_integrity()