"""Pawn-structure evaluation."""


from __future__ import annotations

from chesslab.constants import DOUBLED_PAWN_PENALTY, ISOLATED_PAWN_PENALTY
from chesslab.engine.eval.features import pawn_file_counts
from chesslab.engine.piece import Color
from chesslab.engine.position import Position


def _pawn_structure_for_side(position: Position, color: Color) -> int:
    file_counts = pawn_file_counts(position, color)
    score = 0

    for file_index, count in enumerate(file_counts):
        if count > 1:
            score -= (count - 1) * DOUBLED_PAWN_PENALTY

        if count > 0:
            left_count = file_counts[file_index - 1] if file_index > 0 else 0
            right_count = file_counts[file_index + 1] if file_index < 7 else 0
            if left_count == 0 and right_count == 0:
                score -= count * ISOLATED_PAWN_PENALTY

    return score


def pawn_structure_balance(position: Position) -> int:
    """Return white-minus-black pawn-structure balance."""
    return _pawn_structure_for_side(position, Color.WHITE) - _pawn_structure_for_side(position, Color.BLACK)