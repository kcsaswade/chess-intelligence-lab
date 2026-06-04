from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import coord_to_index
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_white_pawn_attacks_forward_diagonals() -> None:
    position = parse_fen("8/8/8/8/3P4/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("c5"), Color.WHITE)
    assert is_square_attacked(position, coord_to_index("e5"), Color.WHITE)


def test_black_pawn_attacks_forward_diagonals() -> None:
    position = parse_fen("8/8/8/3p4/8/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("c4"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("e4"), Color.BLACK)


def test_pawn_does_not_attack_straight_forward() -> None:
    position = parse_fen("8/8/8/8/3P4/8/8/8 w - - 0 1")
    assert not is_square_attacked(position, coord_to_index("d5"), Color.WHITE)