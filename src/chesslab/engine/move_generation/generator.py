"""Top-level pseudo-legal move generation dispatcher."""

from __future__ import annotations

from chesslab.engine.move import Move
from chesslab.engine.move_generation.king_moves import generate_king_moves
from chesslab.engine.move_generation.knight_moves import generate_knight_moves
from chesslab.engine.move_generation.pawn_moves import generate_pawn_moves
from chesslab.engine.move_generation.slider_moves import generate_slider_moves
from chesslab.engine.piece import PieceType
from chesslab.engine.position import Position


def generate_pseudolegal_moves(position: Position) -> list[Move]:
    """Generate pseudo-legal moves for the side to move only."""
    moves: list[Move] = []

    for square, piece in enumerate(position.board):
        if piece is None or piece.color is not position.side_to_move:
            continue

        if piece.kind is PieceType.PAWN:
            moves.extend(generate_pawn_moves(position, square))
        elif piece.kind is PieceType.KNIGHT:
            moves.extend(generate_knight_moves(position, square))
        elif piece.kind is PieceType.KING:
            moves.extend(generate_king_moves(position, square))
        elif piece.kind in {PieceType.ROOK, PieceType.BISHOP, PieceType.QUEEN}:
            moves.extend(generate_slider_moves(position, square))

    return moves