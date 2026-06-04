"""Small internal validators for early engine debugging."""

from chesslab.constants import BOARD_SIZE
from chesslab.engine.move import Move
from chesslab.engine.position import Position
from chesslab.errors import InvalidMoveError, InvalidSquareError


def assert_valid_square(index: int) -> None:
    """Assert that a square index is on the board."""
    if not 0 <= index < BOARD_SIZE:
        raise InvalidSquareError(f"Square index out of range: {index}")


def assert_move_on_board(move: Move) -> None:
    """Assert that both move endpoints are valid board squares."""
    assert_valid_square(move.from_sq)
    assert_valid_square(move.to_sq)


def assert_piece_exists_at_source(position: Position, move: Move) -> None:
    """Assert that a move source square contains a piece."""
    if position.piece_at(move.from_sq) is None:
        raise InvalidMoveError(f"No piece at source square {move.from_sq}")


def assert_piece_belongs_to_side_to_move(position: Position, move: Move) -> None:
    """Assert that the source piece belongs to the side to move."""
    piece = position.piece_at(move.from_sq)
    if piece is None:
        raise InvalidMoveError(f"No piece at source square {move.from_sq}")
    if piece.color is not position.side_to_move:
        raise InvalidMoveError(
            f"Piece at source square {move.from_sq} does not belong to side to move"
        )