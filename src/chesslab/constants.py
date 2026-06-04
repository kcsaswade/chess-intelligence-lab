"""Project-wide constants used by the application skeleton."""

from chesslab.version import __version__

APP_NAME = "Chess Intelligence Laboratory"
APP_WINDOW_TITLE = f"{APP_NAME} - Stage 1"
CLI_DESCRIPTION = "Foundations of the Chess Intelligence Laboratory"
VERSION_STRING = __version__

DEFAULT_WINDOW_WIDTH = 1024
DEFAULT_WINDOW_HEIGHT = 768

BOARD_SIZE = 64
BOARD_FILES = "abcdefgh"
BOARD_RANKS = "12345678"
START_FEN_FIELD_COUNT = 6

WHITE_PAWN_START_RANK = 1
BLACK_PAWN_START_RANK = 6
WHITE_PROMOTION_RANK = 7
BLACK_PROMOTION_RANK = 0