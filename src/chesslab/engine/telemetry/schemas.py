"""Stable schema helpers/constants."""


from __future__ import annotations

from chesslab.constants import SCHEMA_VERSION

SEARCH_LOG_SCHEMA = "chesslab.search_log"
GAME_LOG_SCHEMA = "chesslab.game_log"


def schema_version() -> str:
    return SCHEMA_VERSION