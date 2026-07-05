"""Oracle tests for FEN parsing and semantic compatibility."""


from __future__ import annotations

from tests.oracles.adapters import python_chess_strict_fen
from tests.oracles.fen_cases import (
    CASTLING_CASES,
    EN_PASSANT_CASES,
    LEGAL_MOVE_CASES,
    PROMOTION_CASES,
    STARTPOS_CASES,
    STATUS_CASES,
)

from chesslab.io.fen import parse_fen, to_fen


def test_start_position_fen_round_trip_matches_python_chess() -> None:
    fen = STARTPOS_CASES[0]["fen"]
    position = parse_fen(fen)
    our_fen = to_fen(position)
    oracle_fen = python_chess_strict_fen(fen)
    assert our_fen == oracle_fen


def test_curated_fens_parse_and_round_trip_semantically() -> None:
    cases = (
        STARTPOS_CASES
        + LEGAL_MOVE_CASES
        + CASTLING_CASES
        + EN_PASSANT_CASES
        + PROMOTION_CASES
        + STATUS_CASES
    )
    for case in cases:
        fen = case["fen"]
        position = parse_fen(fen)
        assert to_fen(position) == python_chess_strict_fen(fen), case["name"]