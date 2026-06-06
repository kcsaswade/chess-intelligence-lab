"""Structured game metadata and record container."""


from __future__ import annotations

from dataclasses import dataclass, field

from chesslab.constants import (
    DEFAULT_PGN_EVENT,
    DEFAULT_PGN_ROUND,
)
from chesslab.engine.game.history import GameHistory


@dataclass
class GameRecord:
    """Serializable game record aligned with PGN metadata."""
    event: str = DEFAULT_PGN_EVENT
    site: str = "Local"
    date: str = "????.??.??"
    round: str = DEFAULT_PGN_ROUND
    white: str = "White"
    black: str = "Black"
    result: str = "*"
    game_id: str = ""
    history: GameHistory = field(default_factory=GameHistory)