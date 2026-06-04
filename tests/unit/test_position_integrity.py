from chesslab.constants import BOARD_SIZE
from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_board_length_remains_64_after_make_unmake() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert len(position.board) == BOARD_SIZE
    assert position.piece_at(coord_to_index("e4")) is None
    assert position.piece_at(coord_to_index("e5")) is not None

    unmake_move(position, move, undo)
    assert len(position.board) == BOARD_SIZE
    assert position.piece_at(coord_to_index("e4")) is not None
    assert position.piece_at(coord_to_index("e5")) is None