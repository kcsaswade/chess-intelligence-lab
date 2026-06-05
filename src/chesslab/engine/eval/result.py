"""Structured evaluation breakdown."""


from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    """Component-based evaluation result."""
    total: int
    material: int
    mobility: int
    king_safety: int
    pawn_structure: int
    center_control: int
    piece_activity: int