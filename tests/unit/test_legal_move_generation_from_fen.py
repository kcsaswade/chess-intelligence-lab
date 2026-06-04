from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_legal_move_count_for_lone_king_position() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert len(generate_legal_moves(position)) == 5


def test_legal_move_count_in_simple_check_position() -> None:
    position = parse_fen("4r3/8/8/8/8/8/8/R3K3 w - - 0 1")
    assert len(generate_legal_moves(position)) == 4


def test_legal_move_count_in_stalemate_position() -> None:
    position = parse_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert len(generate_legal_moves(position)) == 0