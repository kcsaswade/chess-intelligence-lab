"""Evaluation weight definitions."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.constants import (
    DEFAULT_CENTER_CONTROL_WEIGHT,
    DEFAULT_KING_SAFETY_WEIGHT,
    DEFAULT_MATERIAL_WEIGHT,
    DEFAULT_MOBILITY_WEIGHT,
    DEFAULT_PAWN_STRUCTURE_WEIGHT,
    DEFAULT_PIECE_ACTIVITY_WEIGHT,
)


@dataclass(frozen=True)
class EvaluationWeights:
    """Weights for evaluation components."""
    material: int = DEFAULT_MATERIAL_WEIGHT
    mobility: int = DEFAULT_MOBILITY_WEIGHT
    king_safety: int = DEFAULT_KING_SAFETY_WEIGHT
    pawn_structure: int = DEFAULT_PAWN_STRUCTURE_WEIGHT
    center_control: int = DEFAULT_CENTER_CONTROL_WEIGHT
    piece_activity: int = DEFAULT_PIECE_ACTIVITY_WEIGHT