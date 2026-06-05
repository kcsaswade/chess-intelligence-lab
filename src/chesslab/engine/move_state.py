"""Undo state for reversible move application."""

from __future__ import annotations

from dataclasses import dataclass

from chesslab.engine.castling import CastlingRights
from chesslab.engine.piece import Color, Piece


@dataclass
class MoveUndoInfo:
    """All state needed to restore a position after unmaking a move."""

    moved_piece: Piece
    captured_piece: Piece | None
    previous_castling_rights: CastlingRights
    previous_en_passant_square: int | None
    previous_halfmove_clock: int
    previous_fullmove_number: int
    previous_side_to_move: Color
    en_passant_captured_square: int | None = None
    castling_rook_from: int | None = None
    castling_rook_to: int | None = None