"""Material evaluation."""


from __future__ import annotations

from chesslab.constants import (
    BISHOP_VALUE,
    KING_VALUE,
    KNIGHT_VALUE,
    PAWN_VALUE,
    QUEEN_VALUE,
    ROOK_VALUE,
)
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position

_PIECE_VALUES = {
    PieceType.PAWN: PAWN_VALUE,
    PieceType.KNIGHT: KNIGHT_VALUE,
    PieceType.BISHOP: BISHOP_VALUE,
    PieceType.ROOK: ROOK_VALUE,
    PieceType.QUEEN: QUEEN_VALUE,
    PieceType.KING: KING_VALUE,
}


def material_balance(position: Position) -> int:
    """Return white-minus-black material balance."""
    score = 0
    for piece in position.board:
        if piece is None:
            continue
        value = _PIECE_VALUES[piece.kind]
        if piece.color is Color.WHITE:
            score += value
        else:
            score -= value
    return score