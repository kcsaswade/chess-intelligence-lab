"""Evaluation weight definitions."""


from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationWeights:
    """Weights for evaluation components."""
    material: int = 100
    mobility: int = 0
    king_safety: int = 0
    pawn_structure: int = 0
    center_control: int = 0
    piece_activity: int = 0