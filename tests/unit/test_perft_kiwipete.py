from chesslab.engine.perft import perft
from chesslab.io.fen import parse_fen

KIWIPETE_FEN = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"


def test_kiwipete_perft_depth_1() -> None:
    position = parse_fen(KIWIPETE_FEN)
    assert perft(position, 1) == 48


def test_kiwipete_perft_depth_2() -> None:
    position = parse_fen(KIWIPETE_FEN)
    assert perft(position, 2) == 2039