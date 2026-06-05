"""Center-control evaluation."""


from __future__ import annotations

from chesslab.constants import CENTER_ATTACK_BONUS, CENTER_OCCUPATION_BONUS
from chesslab.engine.eval.features import attacked_center_count, occupied_center_count
from chesslab.engine.piece import Color
from chesslab.engine.position import Position


def _center_control_for_side(position: Position, color: Color) -> int:
    return (
        occupied_center_count(position, color) * CENTER_OCCUPATION_BONUS
        + attacked_center_count(position, color) * CENTER_ATTACK_BONUS
    )


def center_control_balance(position: Position) -> int:
    """Return white-minus-black center-control balance."""
    return _center_control_for_side(position, Color.WHITE) - _center_control_for_side(position, Color.BLACK)