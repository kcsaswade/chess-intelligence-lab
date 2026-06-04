from chesslab.engine.attacks import is_square_attacked
from chesslab.engine.board import coord_to_index
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_king_attacks_adjacent_squares() -> None:
    position = parse_fen("8/8/8/8/4k3/8/8/8 w - - 0 1")
    assert is_square_attacked(position, coord_to_index("d3"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("e3"), Color.BLACK)
    assert is_square_attacked(position, coord_to_index("f5"), Color.BLACK)


def test_king_does_not_attack_non_adjacent_square() -> None:
    position = parse_fen("8/8/8/8/4k3/8/8/8 w - - 0 1")
    assert not is_square_attacked(position, coord_to_index("e6"), Color.BLACK)