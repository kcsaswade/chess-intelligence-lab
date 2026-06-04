"""Castling rights representation and FEN conversion."""

from __future__ import annotations

from dataclasses import dataclass

from chesslab.errors import FenError


@dataclass
class CastlingRights:
    """Explicit castling rights container."""

    white_kingside: bool = False
    white_queenside: bool = False
    black_kingside: bool = False
    black_queenside: bool = False

    @classmethod
    def from_fen_field(cls, field: str) -> CastlingRights:
        """Parse castling rights from a FEN field."""
        if field == "-":
            return cls()

        allowed = {"K", "Q", "k", "q"}
        seen: set[str] = set()

        for char in field:
            if char not in allowed:
                raise FenError(f"Invalid castling field: {field!r}")
            if char in seen:
                raise FenError(f"Duplicate castling right in field: {field!r}")
            seen.add(char)

        canonical = "".join(ch for ch in "KQkq" if ch in seen)
        if canonical != field:
            raise FenError(f"Castling field must be ordered as KQkq subset: {field!r}")

        return cls(
            white_kingside="K" in seen,
            white_queenside="Q" in seen,
            black_kingside="k" in seen,
            black_queenside="q" in seen,
        )

    def to_fen_field(self) -> str:
        """Serialize castling rights to a FEN field."""
        rights = []
        if self.white_kingside:
            rights.append("K")
        if self.white_queenside:
            rights.append("Q")
        if self.black_kingside:
            rights.append("k")
        if self.black_queenside:
            rights.append("q")
        return "".join(rights) if rights else "-"