"""Structured game summary telemetry."""


from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from chesslab.constants import VERSION_STRING
from chesslab.engine.telemetry.schemas import GAME_LOG_SCHEMA, schema_version


class _SearchStatsLike(Protocol):
    nodes: int
    depth_reached: int
    time_ms: float



class _HistoryEntryLike(Protocol):
    search_stats: _SearchStatsLike



class _HistoryLike(Protocol):
    entries: list[_HistoryEntryLike]



class _GameRecordLike(Protocol):
    game_id: str
    result: str
    history: _HistoryLike



@dataclass(frozen=True)
class GameLogEntry:
    """Summary of a completed or in-progress game."""
    schema: str
    schema_version: str
    game_id: str
    result: str
    total_plies: int
    average_search_depth: float
    total_nodes: int
    average_move_time_ms: float
    engine_version: str
    timestamp: str



def build_game_log_entry(game_record: _GameRecordLike) -> GameLogEntry:
    entries = game_record.history.entries
    total_plies = len(entries)
    total_nodes = sum(entry.search_stats.nodes for entry in entries)
    average_depth = (
        sum(entry.search_stats.depth_reached for entry in entries) / total_plies
        if total_plies
        else 0.0
    )
    average_move_time = (
        sum(entry.search_stats.time_ms for entry in entries) / total_plies
        if total_plies
        else 0.0
    )

    return GameLogEntry(
        schema=GAME_LOG_SCHEMA,
        schema_version=schema_version(),
        game_id=game_record.game_id,
        result=game_record.result,
        total_plies=total_plies,
        average_search_depth=average_depth,
        total_nodes=total_nodes,
        average_move_time_ms=average_move_time,
        engine_version=VERSION_STRING,
        timestamp=datetime.now(UTC).isoformat(),
    )