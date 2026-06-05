"""Public search entry point."""


from __future__ import annotations

from time import perf_counter

from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.piece import Color
from chesslab.engine.position import Position
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.minimax import search_minimax
from chesslab.engine.search.result import SearchResult
from chesslab.engine.search.stats import SearchStats
from chesslab.engine.search.tracker import SearchTracker


def _to_side_to_move_pov(position: Position, evaluation: EvaluationResult) -> EvaluationResult:
    if position.side_to_move is Color.WHITE:
        return evaluation
    return EvaluationResult(
        total=-evaluation.total,
        material=-evaluation.material,
        mobility=-evaluation.mobility,
        king_safety=-evaluation.king_safety,
        pawn_structure=-evaluation.pawn_structure,
        center_control=-evaluation.center_control,
        piece_activity=-evaluation.piece_activity,
    )


def search_position(position: Position, config: SearchConfig) -> SearchResult:
    """Search a legal position with fixed-depth minimax."""
    start = perf_counter()
    tracker = SearchTracker()

    node_result = search_minimax(
        position=position,
        depth=config.depth,
        config=config,
        tracker=tracker,
    )

    elapsed_ms = (perf_counter() - start) * 1000.0
    best_move = node_result.principal_variation[0] if node_result.principal_variation else None

    root_eval = _to_side_to_move_pov(
        position,
        evaluate(position, config.evaluation_weights),
    )

    stats = SearchStats(
        nodes=tracker.nodes,
        cutoffs=tracker.cutoffs,
        depth_reached=min(config.depth, tracker.max_depth_reached),
        time_ms=elapsed_ms,
        principal_variation=node_result.principal_variation,
    )

    return SearchResult(
        best_move=best_move,
        score=node_result.score,
        stats=stats,
        evaluation=root_eval,
    )