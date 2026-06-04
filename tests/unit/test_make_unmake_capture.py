from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_capture_removes_piece_and_restores_on_unmake() -> None:
    position = parse_fen("8/8/8/4p3/4R3/8/8/8 w - - 7 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("e5"), is_capture=True)

    undo = make_move(position, move)
    assert position.piece_at(coord_to_index("e5")) is not None
    assert position.piece_at(coord_to_index("e4")) is None
    assert position.halfmove_clock == 0

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen