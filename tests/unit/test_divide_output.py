from chesslab.engine.perft import divide, perft
from chesslab.engine.startpos import STARTPOS_FEN
from chesslab.io.fen import parse_fen


def test_divide_sums_to_perft_total() -> None:
    position = parse_fen(STARTPOS_FEN)
    parts = divide(position, 2)
    assert sum(count for _, count in parts) == perft(position, 2)