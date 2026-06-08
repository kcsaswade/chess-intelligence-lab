"""Thin adapters from engine models to GUI display state."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.constants import GUI_READY_TEXT, GUI_THINKING_TEXT
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game.game_controller import GameController
from chesslab.engine.piece import Color
from chesslab.engine.search.stats import SearchStats
from chesslab.io.serializers import move_to_uci


@dataclass(frozen=True)
class GameInfoModel:
    side_to_move: str
    status_text: str
    result_text: str
    engine_state_text: str


@dataclass(frozen=True)
class SearchStatsModel:
    nodes: str
    cutoffs: str
    depth: str
    time_ms: str
    pv: str


def build_game_info_model(controller: GameController, thinking: bool) -> GameInfoModel:
    side_text = "White" if controller.side_to_move is Color.WHITE else "Black"
    return GameInfoModel(
        side_to_move=side_text,
        status_text=controller.status_text(),
        result_text=controller.record.result,
        engine_state_text=GUI_THINKING_TEXT if thinking else GUI_READY_TEXT,
    )


def build_evaluation_lines(evaluation: EvaluationResult) -> list[tuple[str, str]]:
    return [
        ("Total", _format_cp(evaluation.total)),
        ("Material", _format_cp(evaluation.material)),
        ("Mobility", _format_cp(evaluation.mobility)),
        ("King safety", _format_cp(evaluation.king_safety)),
        ("Pawn structure", _format_cp(evaluation.pawn_structure)),
        ("Center control", _format_cp(evaluation.center_control)),
        ("Piece activity", _format_cp(evaluation.piece_activity)),
    ]


def build_search_stats_model(stats: SearchStats) -> SearchStatsModel:
    return SearchStatsModel(
        nodes=str(stats.nodes),
        cutoffs=str(stats.cutoffs),
        depth=str(stats.depth_reached),
        time_ms=f"{stats.time_ms:.1f}",
        pv=" ".join(move_to_uci(move) or "" for move in stats.principal_variation).strip() or "-",
    )


def _format_cp(value: int) -> str:
    return f"{value / 100:.2f}"