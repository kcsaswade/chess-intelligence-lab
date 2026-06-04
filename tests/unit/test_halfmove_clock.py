from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_halfmove_increments_on_quiet_non_pawn_move() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 7 1")
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert position.halfmove_clock == 8

    unmake_move(position, move, undo)
    assert position.halfmove_clock == 7


def test_halfmove_resets_on_pawn_move() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 7 1")
    move = Move(coord_to_index("e2"), coord_to_index("e3"))

    undo = make_move(position, move)
    assert position.halfmove_clock == 0

    unmake_move(position, move, undo)
    assert position.halfmove_clock == 7


def test_halfmove_resets_on_capture() -> None:
    position = parse_fen("8/8/8/4p3/4R3/8/8/8 w - - 7 1")
    move = Move(coord_to_index("e4"), coord_to_index("e5"), is_capture=True)

    undo = make_move(position, move)
    assert position.halfmove_clock == 0

    unmake_move(position, move, undo)
    assert position.halfmove_clock == 7