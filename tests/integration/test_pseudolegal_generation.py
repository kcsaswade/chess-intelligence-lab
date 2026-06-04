from chesslab.engine.move_generation.generator import generate_pseudolegal_moves
from chesslab.io.fen import parse_fen


def test_knight_center_total_moves() -> None:
    position = parse_fen("8/8/8/3N4/8/8/8/8 w - - 0 1")
    assert len(generate_pseudolegal_moves(position)) == 8


def test_king_center_total_moves() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    assert len(generate_pseudolegal_moves(position)) == 8


def test_rook_center_total_moves() -> None:
    position = parse_fen("8/8/8/8/4R3/8/8/8 w - - 0 1")
    assert len(generate_pseudolegal_moves(position)) == 14


def test_bishop_center_total_moves() -> None:
    position = parse_fen("8/8/8/8/3B4/8/8/8 w - - 0 1")
    assert len(generate_pseudolegal_moves(position)) == 13


def test_queen_center_total_moves() -> None:
    position = parse_fen("8/8/8/8/4Q3/8/8/8 w - - 0 1")
    assert len(generate_pseudolegal_moves(position)) == 27