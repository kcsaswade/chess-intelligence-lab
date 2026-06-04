"""Custom exception hierarchy for the project."""


class ChessLabError(Exception):
    """Base exception for all project-specific errors."""


class ConfigurationError(ChessLabError):
    """Raised when configuration is invalid or incomplete."""


class GuiStartupError(ChessLabError):
    """Raised when the GUI cannot be started properly."""


class FenError(ChessLabError):
    """Raised when a FEN string is malformed or cannot be parsed."""


class InvalidSquareError(ChessLabError):
    """Raised when a square coordinate or square index is invalid."""

class InvalidMoveError(ChessLabError):
    """Raised when an internal move application assumption is violated."""