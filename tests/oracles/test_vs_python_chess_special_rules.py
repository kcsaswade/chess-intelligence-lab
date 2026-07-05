"""Special-rule oracle tests for castling, en passant, and promotion."""


from __future__ import annotations

from tests.oracles.fen_cases import CASTLING_CASES, EN_PASSANT_CASES, PROMOTION_CASES
from tests.oracles.move_compare import (
    assert_legal_move_sets_match,
    assert_move_absent_in_both,
    assert_move_present_in_both,
)


def test_castling_cases_match_python_chess() -> None:
    for case in CASTLING_CASES:
        assert_legal_move_sets_match(case["fen"])


def test_en_passant_cases_match_python_chess() -> None:
    for case in EN_PASSANT_CASES:
        assert_legal_move_sets_match(case["fen"])


def test_promotion_cases_match_python_chess() -> None:
    for case in PROMOTION_CASES:
        assert_legal_move_sets_match(case["fen"])


def test_specific_castling_moves() -> None:
    fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
    assert_move_present_in_both(fen, "e1g1")
    assert_move_present_in_both(fen, "e1c1")


def test_specific_en_passant_moves() -> None:
    fen = "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1"
    assert_move_present_in_both(fen, "e5d6")


def test_specific_underpromotion_moves() -> None:
    fen = "4k3/6P1/8/8/8/8/8/4K3 w - - 0 1"
    assert_move_present_in_both(fen, "g7g8q")
    assert_move_present_in_both(fen, "g7g8r")
    assert_move_present_in_both(fen, "g7g8b")
    assert_move_present_in_both(fen, "g7g8n")


def test_illegal_en_passant_due_to_no_target_square() -> None:
    fen = "4k3/8/8/3pP3/8/8/8/4K3 w - - 0 1"
    assert_move_absent_in_both(fen, "e5d6")