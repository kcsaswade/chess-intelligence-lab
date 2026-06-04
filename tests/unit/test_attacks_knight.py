from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import coord_to_index
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_knight_attacks_center_targets() -> None:
    position = parse_fen("8/8/8/3n4/8/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("c3"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("e3"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("f4"), Color.BLACK)


def test_knight_attack_false_when_not_reachable() -> None:
    position = parse_fen("8/8/8/3n4/8/8/8/8 w - - 0 1")
    assert not is_square_attacked(position, coord_to_index("d4"), Color.BLACK)


def test_knight_attacks_from_corner() -> None:
    position = parse_fen("8/8/8/8/8/8/8/n7 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("b3"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("c2"), Color.BLACK)