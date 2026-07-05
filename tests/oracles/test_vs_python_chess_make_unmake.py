"""State-mutation oracle tests against python-chess."""


from __future__ import annotations

from tests.oracles.adapters import make_unmake_our_move_returns_to_same_fen
from tests.oracles.state_compare import assert_resulting_fen_matches


def test_resulting_fen_matches_after_selected_moves() -> None:
    cases = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "g1f3"),
        ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", "e1g1"),
        ("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1", "e5d6"),
        ("4k3/6P1/8/8/8/8/8/4K3 w - - 0 1", "g7g8q"),
    ]
    for fen, uci in cases:
        assert_resulting_fen_matches(fen, uci)


def test_make_unmake_restores_original_fen() -> None:
    cases = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
        ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", "e1c1"),
        ("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1", "e5d6"),
    ]
    for fen, uci in cases:
        assert make_unmake_our_move_returns_to_same_fen(fen, uci), (fen, uci)