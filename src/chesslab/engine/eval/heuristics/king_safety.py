"""Simple king-safety evaluation."""


from __future__ import annotations

from chesslab.constants import (
    CASTLED_KING_BONUS,
    KING_NEARBY_ATTACK_PENALTY,
    KING_OPEN_FILE_PENALTY,
    KING_PAWN_SHIELD_BONUS,
)
from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.eval.features import enemy_of, king_square, pawn_squares
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position


def _pawn_shield_score(position: Position, color: Color) -> int:
    square = king_square(position, color)
    rank, file_index = position.rank_file_of(square)
    forward = 1 if color is Color.WHITE else -1
    shield_rank = rank + forward

    score = 0
    for shield_file in (file_index - 1, file_index, file_index + 1):
        if not is_valid_rank_file(shield_rank, shield_file):
            continue
        shield_square = rank_file_to_index(shield_rank, shield_file)
        piece = position.piece_at(shield_square)
        if piece is not None and piece.color is color and piece.kind is PieceType.PAWN:
            score += KING_PAWN_SHIELD_BONUS
    return score


def _open_file_penalty(position: Position, color: Color) -> int:
    square = king_square(position, color)
    _, file_index = position.rank_file_of(square)
    own_pawn_files = {position.rank_file_of(pawn_square)[1] for pawn_square in pawn_squares(position, color)}
    return 0 if file_index in own_pawn_files else KING_OPEN_FILE_PENALTY


def _nearby_attack_penalty(position: Position, color: Color) -> int:
    square = king_square(position, color)
    rank, file_index = position.rank_file_of(square)
    enemy = enemy_of(color)

    penalty = 0
    for dr in (-1, 0, 1):
        for df in (-1, 0, 1):
            check_rank = rank + dr
            check_file = file_index + df
            if not is_valid_rank_file(check_rank, check_file):
                continue
            zone_square = rank_file_to_index(check_rank, check_file)
            if is_square_attacked(position, zone_square, enemy):
                penalty += KING_NEARBY_ATTACK_PENALTY
    return penalty


def _castled_bonus(position: Position, color: Color) -> int:
    square = king_square(position, color)
    if color is Color.WHITE and square in {6, 2}:
        return CASTLED_KING_BONUS
    if color is Color.BLACK and square in {62, 58}:
        return CASTLED_KING_BONUS
    return 0


def _king_safety_for_side(position: Position, color: Color) -> int:
    return (
        _pawn_shield_score(position, color)
        + _castled_bonus(position, color)
        - _open_file_penalty(position, color)
        - _nearby_attack_penalty(position, color)
    )


def king_safety_balance(position: Position) -> int:
    """Return white-minus-black king safety balance."""
    return _king_safety_for_side(position, Color.WHITE) - _king_safety_for_side(position, Color.BLACK)