"""Minimal deterministic evaluator for Chunk 7."""


from __future__ import annotations

from chesslab.constants import (
    BISHOP_VALUE,
    KING_VALUE,
    KNIGHT_VALUE,
    PAWN_VALUE,
    QUEEN_VALUE,
    ROOK_VALUE,
)
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.eval.weights import EvaluationWeights
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


def _material_balance(position: Position) -> int:
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


def evaluate_position(
    position: Position,
    weights: EvaluationWeights | None = None,
) -> EvaluationResult:
    """Evaluate a position from White's perspective."""
    effective_weights = weights or EvaluationWeights()
    raw_material = _material_balance(position)
    material_score = (raw_material * effective_weights.material) // 100
    return EvaluationResult(
        total=material_score,
        material=material_score,
        mobility=0,
        king_safety=0,
        pawn_structure=0,
        center_control=0,
        piece_activity=0,
    )