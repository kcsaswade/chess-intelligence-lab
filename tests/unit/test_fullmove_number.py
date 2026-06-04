from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_fullmove_not_incremented_after_white_move() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 5")
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert position.fullmove_number == 5

    unmake_move(position, move, undo)
    assert position.fullmove_number == 5


def test_fullmove_incremented_after_black_move() -> None:
    position = parse_fen("8/8/8/8/8/8/8/4k3 b - - 0 5")
    move = Move(coord_to_index("e1"), coord_to_index("e2"))

    undo = make_move(position, move)
    assert position.fullmove_number == 6

    unmake_move(position, move, undo)
    assert position.fullmove_number == 5