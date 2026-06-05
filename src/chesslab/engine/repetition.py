"""Position repetition key helpers."""

from __future__ import annotations

from chesslab.engine.position import Position


def repetition_key(position: Position) -> tuple[tuple[str, ...], str, tuple[bool, bool, bool, bool], int | None]:
    """Return a repetition identity key for the current position."""
    rights = (
        position.castling_rights.white_kingside,
        position.castling_rights.white_queenside,
        position.castling_rights.black_kingside,
        position.castling_rights.black_queenside,
    )
    return (
        position.board_key(),
        position.side_to_move.value,
        rights,
        position.en_passant_square,
    )


def repetition_count(position: Position, history_keys: list[tuple[tuple[str, ...], str, tuple[bool, bool, bool, bool], int | None]]) -> int:
    """Count occurrences of the current repetition key in a history list."""
    current = repetition_key(position)
    return sum(1 for key in history_keys if key == current)