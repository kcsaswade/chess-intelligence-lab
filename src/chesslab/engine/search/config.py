"""Search configuration models."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.constants import DEFAULT_SEARCH_DEPTH
from chesslab.engine.eval.weights import EvaluationWeights


@dataclass(frozen=True)
class SearchConfig:
    """Configuration for fixed-depth search."""
    depth: int = DEFAULT_SEARCH_DEPTH
    use_alpha_beta: bool = True
    evaluation_weights: EvaluationWeights | None = None

    def __post_init__(self) -> None:
        if self.depth < 0:
            raise ValueError("Search depth must be non-negative")