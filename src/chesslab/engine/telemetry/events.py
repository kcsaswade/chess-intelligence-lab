"""Telemetry event dataclasses."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.search.stats import SearchStats


@dataclass(frozen=True)
class SearchEvent:
    """Search completed for a position."""
    game_id: str
    ply: int
    position_fen: str
    score: int
    evaluation: EvaluationResult
    stats: SearchStats
    timestamp: str


@dataclass(frozen=True)
class MoveDecisionEvent:
    """Move selected by the engine."""
    game_id: str
    ply: int
    position_fen: str
    best_move: str
    timestamp: str


@dataclass(frozen=True)
class GameSummaryEvent:
    """End-of-game summary event."""
    game_id: str
    result: str
    total_plies: int
    total_nodes: int
    average_depth: float
    average_move_time_ms: float
    timestamp: str