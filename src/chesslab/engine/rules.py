"""Thin rules-facing façade for legal move and status queries."""

from chesslab.engine.attacks import is_in_check, is_square_attacked
from chesslab.engine.game_status import is_checkmate, is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves

__all__ = [
    "generate_legal_moves",
    "is_checkmate",
    "is_in_check",
    "is_square_attacked",
    "is_stalemate",
]