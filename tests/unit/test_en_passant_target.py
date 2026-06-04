from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_en_passant_set_on_double_push() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    move = Move(
        coord_to_index("e2"),
        coord_to_index("e4"),
        is_double_pawn_push=True,
    )

    undo = make_move(position, move)
    assert position.en_passant_square == coord_to_index("e3")

    unmake_move(position, move, undo)
    assert position.en_passant_square is None


def test_en_passant_cleared_on_non_double_push() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - e3 0 1")
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert position.en_passant_square is None

    unmake_move(position, move, undo)
    assert position.en_passant_square == coord_to_index("e3")