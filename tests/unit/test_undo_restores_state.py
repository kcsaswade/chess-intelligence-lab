from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType
from chesslab.io.fen import parse_fen


def test_quiet_move_roundtrip_restores_exact_fen() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 4 9")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("f5"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)

    assert position.to_fen() == original_fen


def test_capture_roundtrip_restores_exact_fen() -> None:
    position = parse_fen("8/8/8/4p3/4R3/8/8/8 w - - 7 9")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("e5"), is_capture=True)

    undo = make_move(position, move)
    unmake_move(position, move, undo)

    assert position.to_fen() == original_fen


def test_promotion_roundtrip_restores_exact_fen() -> None:
    position = parse_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e7"),
        coord_to_index("e8"),
        promotion=PieceType.QUEEN,
    )

    undo = make_move(position, move)
    unmake_move(position, move, undo)

    assert position.to_fen() == original_fen