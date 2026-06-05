from chesslab.engine.perft import perft
from chesslab.engine.startpos import STARTPOS_FEN
from chesslab.io.fen import parse_fen


def test_start_position_perft_depth_1() -> None:
    position = parse_fen(STARTPOS_FEN)
    assert perft(position, 1) == 20


def test_start_position_perft_depth_2() -> None:
    position = parse_fen(STARTPOS_FEN)
    assert perft(position, 2) == 400


def test_start_position_perft_depth_3() -> None:
    position = parse_fen(STARTPOS_FEN)
    assert perft(position, 3) == 8902