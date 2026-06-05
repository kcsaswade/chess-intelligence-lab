"""Helpers for combining evaluation components consistently."""


from __future__ import annotations

from chesslab.engine.eval.result import EvaluationResult


def scale_component(raw_balance: int, weight: int) -> int:
    """Scale a raw white-minus-black balance by a percentage-like weight."""
    return (raw_balance * weight) // 100


def total_from_components(
    material: int,
    mobility: int,
    king_safety: int,
    pawn_structure: int,
    center_control: int,
    piece_activity: int,
) -> int:
    return (
        material
        + mobility
        + king_safety
        + pawn_structure
        + center_control
        + piece_activity
    )


def build_evaluation_result(
    material: int,
    mobility: int,
    king_safety: int,
    pawn_structure: int,
    center_control: int,
    piece_activity: int,
) -> EvaluationResult:
    return EvaluationResult(
        total=total_from_components(
            material=material,
            mobility=mobility,
            king_safety=king_safety,
            pawn_structure=pawn_structure,
            center_control=center_control,
            piece_activity=piece_activity,
        ),
        material=material,
        mobility=mobility,
        king_safety=king_safety,
        pawn_structure=pawn_structure,
        center_control=center_control,
        piece_activity=piece_activity,
    )