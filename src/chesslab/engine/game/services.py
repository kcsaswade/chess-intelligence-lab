"""Small game-related helpers."""


from __future__ import annotations

from typing import Protocol


class _GameRecordLike(Protocol):
    result: str


def completed_result_or_default(game_record: _GameRecordLike) -> str:
    """Return game result or '*' if unresolved."""
    return game_record.result or "*"