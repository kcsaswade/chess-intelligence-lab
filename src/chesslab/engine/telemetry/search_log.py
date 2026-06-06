"""Structured per-move search telemetry."""


from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from chesslab.constants import VERSION_STRING
from chesslab.engine.position import Position
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.result import SearchResult
from chesslab.engine.telemetry.schemas import SEARCH_LOG_SCHEMA, schema_version
from chesslab.io.fen import to_fen
from chesslab.io.serializers import (
    evaluation_result_to_dict,
    move_to_uci,
    search_config_to_dict,
    search_stats_to_dict,
)


@dataclass(frozen=True)
class SearchLogEntry:
    """Flat but rich search log entry."""
    schema: str
    schema_version: str
    game_id: str
    ply: int
    position_fen: str
    best_move: str | None
    score: int
    eval_components: dict[str, int]
    nodes: int
    cutoffs: int
    depth: int
    time_ms: float
    principal_variation: list[str]
    config: dict[str, Any]
    engine_version: str
    timestamp: str


def build_search_log_entry(
    *,
    game_id: str,
    ply: int,
    position: Position,
    result: SearchResult,
    config: SearchConfig,
) -> SearchLogEntry:
    stats_dict = search_stats_to_dict(result.stats)
    return SearchLogEntry(
        schema=SEARCH_LOG_SCHEMA,
        schema_version=schema_version(),
        game_id=game_id,
        ply=ply,
        position_fen=to_fen(position),
        best_move=move_to_uci(result.best_move),
        score=result.score,
        eval_components=evaluation_result_to_dict(result.evaluation),
        nodes=result.stats.nodes,
        cutoffs=result.stats.cutoffs,
        depth=result.stats.depth_reached,
        time_ms=result.stats.time_ms,
        principal_variation=stats_dict["principal_variation"],
        config=search_config_to_dict(config),
        engine_version=VERSION_STRING,
        timestamp=datetime.now(UTC).isoformat(),
    )