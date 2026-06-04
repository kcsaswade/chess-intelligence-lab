"""Light wrapper around a list of moves."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from chesslab.engine.move import Move


@dataclass
class MoveList:
    """Simple move container with a small convenience API."""

    moves: list[Move] = field(default_factory=list)

    def add(self, move: Move) -> None:
        """Append a move."""
        self.moves.append(move)

    def extend(self, moves: list[Move]) -> None:
        """Extend with another move list."""
        self.moves.extend(moves)

    def captures_only(self) -> list[Move]:
        """Return only capture moves."""
        return [move for move in self.moves if move.is_capture]

    def __iter__(self) -> Iterator[Move]:
        return iter(self.moves)

    def __len__(self) -> int:
        return len(self.moves)