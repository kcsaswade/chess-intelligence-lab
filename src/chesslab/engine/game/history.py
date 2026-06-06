"""Move-by-move game history structures."""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.move import Move
from chesslab.engine.search.stats import SearchStats


@dataclass(frozen=True)
class GameHistoryEntry:
    """Single recorded ply in a game history."""
    ply: int
    move: Move
    fen_before: str
    fen_after: str
    evaluation: EvaluationResult
    search_stats: SearchStats
    san: str | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


@dataclass
class GameHistory:
    """Ordered history of played moves."""
    entries: list[GameHistoryEntry] = field(default_factory=list)

    def append(self, entry: GameHistoryEntry) -> None:
        self.entries.append(entry)

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self.entries)

    @property
    def ply_count(self) -> int:
        return len(self.entries)