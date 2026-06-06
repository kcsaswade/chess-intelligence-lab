"""Minimal PGN export."""


from __future__ import annotations

from typing import Protocol

from chesslab.engine.game.services import completed_result_or_default


class _HistoryEntryLike(Protocol):
    san: str | None


class _HistoryLike(Protocol):
    entries: list[_HistoryEntryLike]


class _GameRecordLike(Protocol):
    event: str
    site: str
    date: str
    round: str
    white: str
    black: str
    result: str
    history: _HistoryLike


_REQUIRED_TAGS = ("Event", "Site", "Date", "Round", "White", "Black", "Result")


def _tag_pair(name: str, value: str) -> str:
    return f'[{name} "{value}"]'


def export_pgn(game_record: _GameRecordLike) -> str:
    tags = [
        _tag_pair("Event", game_record.event),
        _tag_pair("Site", game_record.site),
        _tag_pair("Date", game_record.date),
        _tag_pair("Round", game_record.round),
        _tag_pair("White", game_record.white),
        _tag_pair("Black", game_record.black),
        _tag_pair("Result", completed_result_or_default(game_record)),
    ]

    moves: list[str] = []
    for index, entry in enumerate(game_record.history.entries):
        if index % 2 == 0:
            move_number = (index // 2) + 1
            moves.append(f"{move_number}. {entry.san or ''}".strip())
        else:
            moves.append(entry.san or "")

    movetext = " ".join(part for part in moves if part)
    result = completed_result_or_default(game_record)
    if movetext:
        movetext = f"{movetext} {result}"
    else:
        movetext = result

    return "\n".join(tags) + "\n\n" + movetext + "\n"