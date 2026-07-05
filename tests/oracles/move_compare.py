"""Helpers for comparing legal move sets against python-chess."""


from __future__ import annotations

from tests.oracles.adapters import (
    our_legal_moves_uci,
    python_chess_legal_moves_uci,
)


def assert_legal_move_sets_match(fen: str) -> None:
    ours = our_legal_moves_uci(fen)
    oracle = python_chess_legal_moves_uci(fen)
    assert ours == oracle, (
        f"Legal move mismatch for FEN:\n{fen}\n"
        f"Only ours: {sorted(ours - oracle)}\n"
        f"Only python-chess: {sorted(oracle - ours)}"
    )


def assert_move_present_in_both(fen: str, uci: str) -> None:
    ours = our_legal_moves_uci(fen)
    oracle = python_chess_legal_moves_uci(fen)
    assert uci in ours, f"{uci} missing from our legal moves for FEN: {fen}"
    assert uci in oracle, f"{uci} missing from python-chess legal moves for FEN: {fen}"


def assert_move_absent_in_both(fen: str, uci: str) -> None:
    ours = our_legal_moves_uci(fen)
    oracle = python_chess_legal_moves_uci(fen)
    assert uci not in ours, f"{uci} unexpectedly legal in our engine for FEN: {fen}"
    assert uci not in oracle, f"{uci} unexpectedly legal in python-chess for FEN: {fen}"