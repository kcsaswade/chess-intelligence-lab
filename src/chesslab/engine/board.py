"""Board indexing helpers and board container validation."""

from __future__ import annotations

from collections.abc import Sequence

from chesslab.constants import BOARD_FILES, BOARD_RANKS, BOARD_SIZE
from chesslab.errors import InvalidSquareError
from chesslab.types import SquareIndex


def rank_file_to_index(rank: int, file: int) -> SquareIndex:
    """Convert zero-based rank/file to square index using a1=0 mapping."""
    if not (0 <= rank < 8):
        raise InvalidSquareError(f"Rank out of range: {rank}")
    if not (0 <= file < 8):
        raise InvalidSquareError(f"File out of range: {file}")
    return rank * 8 + file


def index_to_rank_file(index: int) -> tuple[int, int]:
    """Convert square index to zero-based rank/file."""
    if not (0 <= index < BOARD_SIZE):
        raise InvalidSquareError(f"Square index out of range: {index}")
    rank = index // 8
    file = index % 8
    return rank, file


def coord_to_index(coord: str) -> SquareIndex:
    """Convert algebraic coordinate like 'e4' to a square index."""
    if len(coord) != 2:
        raise InvalidSquareError(f"Invalid square coordinate: {coord!r}")

    file_char = coord[0]
    rank_char = coord[1]

    if file_char not in BOARD_FILES or rank_char not in BOARD_RANKS:
        raise InvalidSquareError(f"Invalid square coordinate: {coord!r}")

    file = BOARD_FILES.index(file_char)
    rank = int(rank_char) - 1
    return rank_file_to_index(rank, file)


def index_to_coord(index: int) -> str:
    """Convert square index to algebraic coordinate."""
    rank, file = index_to_rank_file(index)
    return f"{BOARD_FILES[file]}{rank + 1}"


def is_valid_rank_file(rank: int, file: int) -> bool:
    """Return whether zero-based rank/file lies on the board."""
    return 0 <= rank < 8 and 0 <= file < 8


def validate_board_squares(board: Sequence[object | None]) -> None:
    """Validate a board-like sequence has exactly 64 entries."""
    if len(board) != BOARD_SIZE:
        raise ValueError(f"Board must contain exactly {BOARD_SIZE} squares, got {len(board)}")