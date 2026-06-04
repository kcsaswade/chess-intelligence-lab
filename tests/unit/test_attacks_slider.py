from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import coord_to_index
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_rook_attack_unobstructed() -> None:
    position = parse_fen("8/8/8/8/4r3/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("e1"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("a4"), Color.BLACK)


def test_rook_attack_blocked_by_piece() -> None:
    position = parse_fen("8/8/8/8/4r3/4p3/8/4K3 w - - 0 1")
    assert not is_square_attacked(position, coord_to_index("e1"), Color.BLACK)


def test_bishop_attack_unobstructed() -> None:
    position = parse_fen("8/8/8/8/3b4/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("a1"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("g1"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("a7"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("h8"), Color.BLACK)


def test_bishop_attack_blocked_by_piece() -> None:
    position = parse_fen("8/8/8/8/3b4/2p5/8/8 w - - 0 1")
    # Blocked diagonal: d4-c3-b2-a1; bishop must not attack beyond c3.
    assert not is_square_attacked(position, coord_to_index("a1"), Color.BLACK)


def test_queen_attacks_as_slider_union() -> None:
    position = parse_fen("8/8/8/8/4q3/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("e1"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("b7"), Color.BLACK)