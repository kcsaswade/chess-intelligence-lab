"""Engine-wide move representation."""

from __future__ import annotations

from dataclasses import dataclass

from chesslab.engine.piece import PieceType
from chesslab.types import SquareIndex


@dataclass(frozen=True)
class Move:
    """Immutable engine move object."""

    from_sq: SquareIndex
    to_sq: SquareIndex
    promotion: PieceType | None = None
    is_capture: bool = False
    is_castling: bool = False
    is_en_passant: bool = False
    is_double_pawn_push: bool = False

    def is_promotion(self) -> bool:
        """Return whether this move is a promotion."""
        return self.promotion is not None