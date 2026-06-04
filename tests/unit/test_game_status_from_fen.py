from chesslab.engine.attacks import is_in_check
from chesslab.engine.game_status import is_checkmate, is_stalemate
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_check_status_from_fen() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4r3/4K3 w - - 0 1")
    assert is_in_check(position, Color.WHITE)


def test_checkmate_status_from_fen() -> None:
    position = parse_fen("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")
    assert is_checkmate(position)


def test_stalemate_status_from_fen() -> None:
    position = parse_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert is_stalemate(position)