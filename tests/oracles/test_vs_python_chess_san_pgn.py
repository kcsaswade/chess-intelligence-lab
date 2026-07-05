"""Spot checks for SAN and PGN behavior against python-chess."""


from __future__ import annotations

from tests.oracles.adapters import (
    python_chess_play_line_to_pgn,
    uci_to_our_move,
)
from tests.oracles.state_compare import assert_san_matches

from chesslab.engine.game.game_controller import GameController
from chesslab.engine.position import Position
from chesslab.io.pgn import export_pgn


def test_selected_san_strings_match_python_chess() -> None:
    cases = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "g1f3"),
        ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", "e1g1"),
        ("4k3/6P1/8/8/8/8/8/4K3 w - - 0 1", "g7g8q"),
    ]
    for fen, uci in cases:
        assert_san_matches(fen, uci)


def test_minimal_pgn_semantically_aligns_for_short_line() -> None:
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    uci_moves = ["e2e4", "e7e5", "g1f3", "b8c6"]

    controller = GameController(Position.from_fen(start_fen))
    for uci in uci_moves:
        move = uci_to_our_move(controller.position, uci)
        controller.apply_move(move)

    our_pgn = export_pgn(controller.record)
    oracle_pgn, oracle_san_moves, oracle_result = python_chess_play_line_to_pgn(start_fen, uci_moves)

    for san in oracle_san_moves:
        assert san in our_pgn
    assert controller.record.result == oracle_result
    assert '[Result "*"]' in our_pgn