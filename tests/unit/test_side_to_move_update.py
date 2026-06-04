from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_side_to_move_flips_and_restores() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert position.side_to_move is Color.BLACK

    unmake_move(position, move, undo)
    assert position.side_to_move is Color.WHITE