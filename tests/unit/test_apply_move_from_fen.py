from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_apply_white_double_push_from_fen() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    move = Move(
        coord_to_index("e2"),
        coord_to_index("e4"),
        is_double_pawn_push=True,
    )

    make_move(position, move)
    assert position.to_fen() == "8/8/8/8/4P3/8/8/8 b - e3 0 1"


def test_apply_black_quiet_move_from_fen() -> None:
    position = parse_fen("8/8/8/8/8/8/8/4k3 b - - 4 5")
    move = Move(coord_to_index("e1"), coord_to_index("e2"))

    make_move(position, move)
    assert position.to_fen() == "8/8/8/8/8/8/4k3/8 w - - 5 6"