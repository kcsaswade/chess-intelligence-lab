from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_white_double_push_sets_en_passant_and_unmakes() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e2"),
        coord_to_index("e4"),
        is_double_pawn_push=True,
    )

    undo = make_move(position, move)
    assert position.en_passant_square == coord_to_index("e3")

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_black_double_push_sets_en_passant_and_unmakes() -> None:
    position = parse_fen("8/4p3/8/8/8/8/8/8 b - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e7"),
        coord_to_index("e5"),
        is_double_pawn_push=True,
    )

    undo = make_move(position, move)
    assert position.en_passant_square == coord_to_index("e6")

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen