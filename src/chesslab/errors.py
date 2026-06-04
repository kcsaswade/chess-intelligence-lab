"""Custom exception hierarchy for the project."""

class ChessLabError(Exception):
    """Base exception for all project-specific errors."""


class ConfigurationError(ChessLabError):
    """Raised when configuration is invalid or incomplete."""


class GuiStartupError(ChessLabError):
    """Raised when the GUI cannot be started properly."""