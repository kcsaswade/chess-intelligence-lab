from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_en_passant_make_unmake_restores_fen() -> None:
    position = parse_fen("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1")
    fen_before = position.to_fen()

    move = Move(
        from_sq=coord_to_index("e5"),
        to_sq=coord_to_index("d6"),
        is_capture=True,
        is_en_passant=True,
    )
    undo = make_move(position, move)

    assert position.piece_at(coord_to_index("d6")) is not None
    assert position.piece_at(coord_to_index("d5")) is None

    unmake_move(position, move, undo)
    assert position.to_fen() == fen_before