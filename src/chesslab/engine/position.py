"""Canonical chess position state."""

from __future__ import annotations

from dataclasses import dataclass, field

from chesslab.constants import BOARD_SIZE
from chesslab.engine.board import index_to_rank_file, validate_board_squares
from chesslab.engine.castling import CastlingRights
from chesslab.engine.piece import Color, Piece
from chesslab.types import SquareIndex


@dataclass
class Position:
    """Complete FEN-representable chess position."""

    board: list[Piece | None] = field(default_factory=lambda: [None] * BOARD_SIZE)
    side_to_move: Color = Color.WHITE
    castling_rights: CastlingRights = field(default_factory=CastlingRights)
    en_passant_square: SquareIndex | None = None
    halfmove_clock: int = 0
    fullmove_number: int = 1

    def __post_init__(self) -> None:
        validate_board_squares(self.board)

    def piece_at(self, square: SquareIndex) -> Piece | None:
        """Return the piece at a square index."""
        return self.board[square]

    def set_piece(self, square: SquareIndex, piece: Piece | None) -> None:
        """Set a piece at a square index."""
        self.board[square] = piece

    def rank_file_of(self, square: SquareIndex) -> tuple[int, int]:
        """Return zero-based rank/file for a square."""
        return index_to_rank_file(square)

    def copy_shallow(self) -> Position:
        """Return a shallow copy of the position state."""
        return Position(
            board=self.board.copy(),
            side_to_move=self.side_to_move,
            castling_rights=CastlingRights(
                white_kingside=self.castling_rights.white_kingside,
                white_queenside=self.castling_rights.white_queenside,
                black_kingside=self.castling_rights.black_kingside,
                black_queenside=self.castling_rights.black_queenside,
            ),
            en_passant_square=self.en_passant_square,
            halfmove_clock=self.halfmove_clock,
            fullmove_number=self.fullmove_number,
        )

    @classmethod
    def from_fen(cls, fen: str) -> Position:
        """Create a position from FEN through the IO boundary."""
        from chesslab.io.fen import parse_fen

        return parse_fen(fen)

    def to_fen(self) -> str:
        """Serialize the position to FEN through the IO boundary."""
        from chesslab.io.fen import to_fen

        return to_fen(self)