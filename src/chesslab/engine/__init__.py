"""Core engine package exports."""

from chesslab.engine.attacks import is_in_check, is_square_attacked
from chesslab.engine.castling import CastlingRights
from chesslab.engine.game_status import is_checkmate, is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves, is_legal_move
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.move_state import MoveUndoInfo
from chesslab.engine.piece import Color, Piece, PieceType
from chesslab.engine.position import Position
from chesslab.engine.startpos import STARTPOS_FEN

__all__ = [
    "CastlingRights",
    "Color",
    "Move",
    "MoveUndoInfo",
    "Piece",
    "PieceType",
    "Position",
    "STARTPOS_FEN",
    "generate_legal_moves",
    "is_checkmate",
    "is_in_check",
    "is_legal_move",
    "is_square_attacked",
    "is_stalemate",
    "make_move",
    "unmake_move",
]