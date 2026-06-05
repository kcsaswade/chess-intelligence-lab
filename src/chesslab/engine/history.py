"""Lightweight position-history support for repetition tracking."""

from __future__ import annotations

from dataclasses import dataclass, field

from chesslab.engine.position import Position
from chesslab.engine.repetition import repetition_key


@dataclass
class PositionHistory:
    """Append-only repetition-key history."""

    keys: list[tuple[tuple[str, ...], str, tuple[bool, bool, bool, bool], int | None]] = field(
        default_factory=list
    )

    @classmethod
    def from_position(cls, position: Position) -> PositionHistory:
        return cls(keys=[repetition_key(position)])

    def record(self, position: Position) -> None:
        self.keys.append(repetition_key(position))

    def count_current(self, position: Position) -> int:
        current = repetition_key(position)
        return sum(1 for key in self.keys if key == current)