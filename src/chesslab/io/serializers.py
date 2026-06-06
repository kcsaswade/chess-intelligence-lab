"""Stable serializers for logs and exports."""


from __future__ import annotations

from dataclasses import asdict
from typing import Any, Protocol

from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.move import Move
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.stats import SearchStats


class _SearchLogLike(Protocol):
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


class _GameLogLike(Protocol):
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


def move_to_uci(move: Move | None) -> str | None:
    if move is None:
        return None

    files = "abcdefgh"
    ranks = "12345678"

    def square_to_text(square: int) -> str:
        file_index = square % 8
        rank_index = square // 8
        return f"{files[file_index]}{ranks[rank_index]}"

    text = f"{square_to_text(move.from_sq)}{square_to_text(move.to_sq)}"
    if move.promotion is not None:
        text += move.promotion.value
    return text


def evaluation_result_to_dict(result: EvaluationResult) -> dict[str, int]:
    return {
        "total": result.total,
        "material": result.material,
        "mobility": result.mobility,
        "king_safety": result.king_safety,
        "pawn_structure": result.pawn_structure,
        "center_control": result.center_control,
        "piece_activity": result.piece_activity,
    }


def search_stats_to_dict(stats: SearchStats) -> dict[str, Any]:
    return {
        "nodes": stats.nodes,
        "cutoffs": stats.cutoffs,
        "depth_reached": stats.depth_reached,
        "time_ms": stats.time_ms,
        "principal_variation": [move_to_uci(move) for move in stats.principal_variation],
    }


def search_config_to_dict(config: SearchConfig) -> dict[str, Any]:
    return {
        "depth": config.depth,
        "use_alpha_beta": config.use_alpha_beta,
        "evaluation_weights": (
            asdict(config.evaluation_weights)
            if config.evaluation_weights is not None
            else None
        ),
    }


def search_log_entry_to_dict(entry: _SearchLogLike) -> dict[str, Any]:
    return {
        "schema": entry.schema,
        "schema_version": entry.schema_version,
        "game_id": entry.game_id,
        "ply": entry.ply,
        "position_fen": entry.position_fen,
        "best_move": entry.best_move,
        "score": entry.score,
        "eval_components": entry.eval_components,
        "nodes": entry.nodes,
        "cutoffs": entry.cutoffs,
        "depth": entry.depth,
        "time_ms": entry.time_ms,
        "principal_variation": entry.principal_variation,
        "config": entry.config,
        "engine_version": entry.engine_version,
        "timestamp": entry.timestamp,
    }


def game_log_entry_to_dict(entry: _GameLogLike) -> dict[str, Any]:
    return {
        "schema": entry.schema,
        "schema_version": entry.schema_version,
        "game_id": entry.game_id,
        "result": entry.result,
        "total_plies": entry.total_plies,
        "average_search_depth": entry.average_search_depth,
        "total_nodes": entry.total_nodes,
        "average_move_time_ms": entry.average_move_time_ms,
        "engine_version": entry.engine_version,
        "timestamp": entry.timestamp,
    }