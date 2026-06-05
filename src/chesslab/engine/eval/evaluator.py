"""Deterministic component-based evaluator for Chunk 8."""


from __future__ import annotations

from chesslab.engine.eval.heuristics.center_control import center_control_balance
from chesslab.engine.eval.heuristics.king_safety import king_safety_balance
from chesslab.engine.eval.heuristics.material import material_balance
from chesslab.engine.eval.heuristics.mobility import mobility_balance
from chesslab.engine.eval.heuristics.pawn_structure import pawn_structure_balance
from chesslab.engine.eval.heuristics.piece_activity import piece_activity_balance
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.eval.scoring import build_evaluation_result, scale_component
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.engine.position import Position


def evaluate(position: Position, weights: EvaluationWeights | None = None) -> EvaluationResult:
    """Evaluate a position from White's perspective with component breakdown."""
    effective_weights = weights or EvaluationWeights()

    material = scale_component(material_balance(position), effective_weights.material)
    mobility = scale_component(mobility_balance(position), effective_weights.mobility)
    king_safety = scale_component(king_safety_balance(position), effective_weights.king_safety)
    pawn_structure = scale_component(
        pawn_structure_balance(position),
        effective_weights.pawn_structure,
    )
    center_control = scale_component(
        center_control_balance(position),
        effective_weights.center_control,
    )
    piece_activity = scale_component(
        piece_activity_balance(position),
        effective_weights.piece_activity,
    )

    return build_evaluation_result(
        material=material,
        mobility=mobility,
        king_safety=king_safety,
        pawn_structure=pawn_structure,
        center_control=center_control,
        piece_activity=piece_activity,
    )


def evaluate_position(
    position: Position,
    weights: EvaluationWeights | None = None,
) -> EvaluationResult:
    """Backward-compatible alias for the public evaluator."""
    return evaluate(position, weights)