from chesslab.engine.game_status import is_checkmate, is_stalemate
from chesslab.io.fen import parse_fen


def test_ordinary_position_is_neither_mate_nor_stalemate() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert not is_checkmate(position)
    assert not is_stalemate(position)


def test_checked_but_escapable_is_not_mate() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4r3/3K4 w - - 0 1")
    assert not is_checkmate(position)


def test_not_checked_with_legal_moves_is_not_stalemate() -> None:
    position = parse_fen("7k/8/6K1/8/8/8/8/8 b - - 0 1")
    assert not is_stalemate(position)