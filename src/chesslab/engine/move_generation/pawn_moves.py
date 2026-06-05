"""Pawn pseudo-legal move generation."""

from __future__ import annotations

from chesslab.constants import (
    BLACK_PAWN_START_RANK,
    BLACK_PROMOTION_RANK,
    WHITE_PAWN_START_RANK,
    WHITE_PROMOTION_RANK,
)
from chesslab.engine.board import is_valid_rank_file, rank_file_to_index
from chesslab.engine.move import Move
from chesslab.engine.move_generation.filters import is_empty, is_enemy_piece
from chesslab.engine.piece import Color, PieceType
from chesslab.engine.position import Position


def _promotion_pieces() -> tuple[PieceType, ...]:
    return (
        PieceType.QUEEN,
        PieceType.ROOK,
        PieceType.BISHOP,
        PieceType.KNIGHT,
    )


def generate_pawn_moves(position: Position, from_sq: int) -> list[Move]:
    """Generate pseudo-legal pawn moves from a square, including en passant."""
    piece = position.piece_at(from_sq)
    if piece is None or piece.kind is not PieceType.PAWN:
        return []

    rank, file = position.rank_file_of(from_sq)
    moves: list[Move] = []

    if piece.color is Color.WHITE:
        forward_delta = 1
        start_rank = WHITE_PAWN_START_RANK
        promotion_rank = WHITE_PROMOTION_RANK
        capture_deltas = ((1, -1), (1, 1))
    else:
        forward_delta = -1
        start_rank = BLACK_PAWN_START_RANK
        promotion_rank = BLACK_PROMOTION_RANK
        capture_deltas = ((-1, -1), (-1, 1))

    one_step_rank = rank + forward_delta
    if is_valid_rank_file(one_step_rank, file):
        one_step_sq = rank_file_to_index(one_step_rank, file)
        if is_empty(position, one_step_sq):
            if one_step_rank == promotion_rank:
                for promotion_piece in _promotion_pieces():
                    moves.append(
                        Move(
                            from_sq=from_sq,
                            to_sq=one_step_sq,
                            promotion=promotion_piece,
                        )
                    )
            else:
                moves.append(Move(from_sq=from_sq, to_sq=one_step_sq))

                two_step_rank = rank + (2 * forward_delta)
                if rank == start_rank and is_valid_rank_file(two_step_rank, file):
                    two_step_sq = rank_file_to_index(two_step_rank, file)
                    if is_empty(position, two_step_sq):
                        moves.append(
                            Move(
                                from_sq=from_sq,
                                to_sq=two_step_sq,
                                is_double_pawn_push=True,
                            )
                        )

    for rank_delta, file_delta in capture_deltas:
        target_rank = rank + rank_delta
        target_file = file + file_delta

        if not is_valid_rank_file(target_rank, target_file):
            continue

        to_sq = rank_file_to_index(target_rank, target_file)
        if is_enemy_piece(position, to_sq, piece.color):
            if target_rank == promotion_rank:
                for promotion_piece in _promotion_pieces():
                    moves.append(
                        Move(
                            from_sq=from_sq,
                            to_sq=to_sq,
                            promotion=promotion_piece,
                            is_capture=True,
                        )
                    )
            else:
                moves.append(Move(from_sq=from_sq, to_sq=to_sq, is_capture=True))

        if position.en_passant_square == to_sq:
            moves.append(
                Move(
                    from_sq=from_sq,
                    to_sq=to_sq,
                    is_capture=True,
                    is_en_passant=True,
                )
            )

    return moves