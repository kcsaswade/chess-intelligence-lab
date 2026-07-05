"""Helpers for comparing resulting state against python-chess."""


from __future__ import annotations

from tests.oracles.adapters import (
    apply_our_move_and_get_fen,
    apply_python_chess_move_and_get_fen,
    our_san_for_move,
    our_status,
    python_chess_san_for_move,
    python_chess_status,
)


def assert_resulting_fen_matches(fen: str, uci: str) -> None:
    our_fen = apply_our_move_and_get_fen(fen, uci)
    oracle_fen = apply_python_chess_move_and_get_fen(fen, uci)
    assert our_fen == oracle_fen, (
        f"Resulting FEN mismatch for move {uci} from:\n{fen}\n"
        f"Our FEN: {our_fen}\n"
        f"Oracle FEN: {oracle_fen}"
    )


def assert_status_matches(fen: str) -> None:
    ours = our_status(fen)
    oracle = python_chess_status(fen)
    assert ours["is_checkmate"] == oracle["is_checkmate"], (
        f"Checkmate mismatch for FEN:\n{fen}\nours={ours}\noracle={oracle}"
    )
    assert ours["is_stalemate"] == oracle["is_stalemate"], (
        f"Stalemate mismatch for FEN:\n{fen}\nours={ours}\noracle={oracle}"
    )


def assert_san_matches(fen: str, uci: str) -> None:
    our_san = our_san_for_move(fen, uci)
    oracle_san = python_chess_san_for_move(fen, uci)
    assert our_san == oracle_san, (
        f"SAN mismatch for move {uci} from:\n{fen}\n"
        f"Our SAN: {our_san}\n"
        f"Oracle SAN: {oracle_san}"
    )