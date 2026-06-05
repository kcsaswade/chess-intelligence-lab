"""Top-level search result model."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.move import Move
from chesslab.engine.search.stats import SearchStats


@dataclass(frozen=True)
class SearchResult:
    """Public result for a completed search."""
    best_move: Move | None
    score: int
    stats: SearchStats
    evaluation: EvaluationResult