"""Chess piece domain models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from chesslab.errors import FenError


class Color(StrEnum):
    """Chess side colors."""

    WHITE = "w"
    BLACK = "b"

    @property
    def opposite(self) -> Color:
        """Return the opposite color."""
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class PieceType(StrEnum):
    """Chess piece kinds."""

    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"


@dataclass(frozen=True)
class Piece:
    """Immutable piece value object."""

    color: Color
    kind: PieceType

    @classmethod
    def from_fen_char(cls, char: str) -> Piece:
        """Create a piece from a single FEN piece character."""
        if len(char) != 1 or not char.isalpha():
            raise FenError(f"Invalid FEN piece character: {char!r}")

        color = Color.WHITE if char.isupper() else Color.BLACK
        symbol = char.lower()

        try:
            kind = PieceType(symbol)
        except ValueError as exc:
            raise FenError(f"Invalid FEN piece character: {char!r}") from exc

        return cls(color=color, kind=kind)

    def to_fen_char(self) -> str:
        """Convert the piece to a single FEN piece character."""
        symbol = self.kind.value
        return symbol.upper() if self.color is Color.WHITE else symbol