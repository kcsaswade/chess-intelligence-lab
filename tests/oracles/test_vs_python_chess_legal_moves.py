"""Core legal-move oracle tests."""


from __future__ import annotations

from tests.oracles.fen_cases import LEGAL_MOVE_CASES, STARTPOS_CASES
from tests.oracles.move_compare import assert_legal_move_sets_match


def test_start_position_legal_moves_match_python_chess() -> None:
    fen = STARTPOS_CASES[0]["fen"]
    assert_legal_move_sets_match(fen)


def test_curated_legal_move_positions_match_python_chess() -> None:
    for case in LEGAL_MOVE_CASES:
        assert_legal_move_sets_match(case["fen"])