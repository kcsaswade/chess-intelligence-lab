"""Fixed-depth minimax with optional alpha-beta pruning."""


from __future__ import annotations

from dataclasses import dataclass

from chesslab.constants import DRAW_SCORE, MATE_SCORE
from chesslab.engine.eval.evaluator import evaluate_position
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game_status import is_checkmate, is_draw, is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import Color
from chesslab.engine.position import Position
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.ordering import order_moves
from chesslab.engine.search.pv import prepend_pv
from chesslab.engine.search.tracker import SearchTracker


@dataclass(frozen=True)
class _SearchNodeResult:
    score: int
    principal_variation: list[Move]


def _terminal_score(position: Position, ply: int) -> int | None:
    if is_checkmate(position):
        return -MATE_SCORE + ply
    if is_stalemate(position):
        return DRAW_SCORE
    if is_draw(position):
        return DRAW_SCORE
    return None


def _evaluate_for_side_to_move(
    position: Position,
    config: SearchConfig,
) -> EvaluationResult:
    white_pov = evaluate_position(position, config.evaluation_weights)
    if position.side_to_move is Color.WHITE:
        return white_pov
    return EvaluationResult(
        total=-white_pov.total,
        material=-white_pov.material,
        mobility=-white_pov.mobility,
        king_safety=-white_pov.king_safety,
        pawn_structure=-white_pov.pawn_structure,
        center_control=-white_pov.center_control,
        piece_activity=-white_pov.piece_activity,
    )


def search_minimax(
    position: Position,
    depth: int,
    config: SearchConfig,
    tracker: SearchTracker,
    ply: int = 0,
    alpha: int = -MATE_SCORE,
    beta: int = MATE_SCORE,
) -> _SearchNodeResult:
    """Search a position and return score plus principal variation."""
    tracker.record_node(ply)

    terminal = _terminal_score(position, ply)
    if terminal is not None:
        return _SearchNodeResult(score=terminal, principal_variation=[])

    if depth == 0:
        evaluation = _evaluate_for_side_to_move(position, config)
        return _SearchNodeResult(score=evaluation.total, principal_variation=[])

    legal_moves = generate_legal_moves(position)
    if not legal_moves:
        terminal_no_moves = _terminal_score(position, ply)
        if terminal_no_moves is None:
            terminal_no_moves = DRAW_SCORE
        return _SearchNodeResult(score=terminal_no_moves, principal_variation=[])

    ordered_moves = order_moves(position, legal_moves)
    best_score = -MATE_SCORE
    best_pv: list[Move] = []

    current_alpha = alpha
    current_beta = beta

    for move in ordered_moves:
        undo = make_move(position, move)
        try:
            child = search_minimax(
                position=position,
                depth=depth - 1,
                config=config,
                tracker=tracker,
                ply=ply + 1,
                alpha=-current_beta if config.use_alpha_beta else -MATE_SCORE,
                beta=-current_alpha if config.use_alpha_beta else MATE_SCORE,
            )
        finally:
            unmake_move(position, move, undo)

        score = -child.score
        if score > best_score:
            best_score = score
            best_pv = prepend_pv(move, child.principal_variation)

        if config.use_alpha_beta:
            if score > current_alpha:
                current_alpha = score
            if current_alpha >= current_beta:
                tracker.record_cutoff()
                break

    return _SearchNodeResult(score=best_score, principal_variation=best_pv)