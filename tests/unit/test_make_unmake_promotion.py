from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType
from chesslab.io.fen import parse_fen


def test_white_promotion_make_unmake_restores_pawn() -> None:
    position = parse_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e7"),
        coord_to_index("e8"),
        promotion=PieceType.QUEEN,
    )

    undo = make_move(position, move)
    assert position.piece_at(coord_to_index("e8")) is not None
    assert position.piece_at(coord_to_index("e8")).kind is PieceType.QUEEN

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_black_promotion_make_unmake_restores_pawn() -> None:
    position = parse_fen("8/8/8/8/8/8/4p3/8 b - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e2"),
        coord_to_index("e1"),
        promotion=PieceType.ROOK,
    )

    undo = make_move(position, move)
    assert position.piece_at(coord_to_index("e1")) is not None
    assert position.piece_at(coord_to_index("e1")).kind is PieceType.ROOK

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_promotion_capture_make_unmake_restores_state() -> None:
    position = parse_fen("3r4/4P3/8/8/8/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(
        coord_to_index("e7"),
        coord_to_index("d8"),
        promotion=PieceType.KNIGHT,
        is_capture=True,
    )

    undo = make_move(position, move)
    assert position.piece_at(coord_to_index("d8")) is not None
    assert position.piece_at(coord_to_index("d8")).kind is PieceType.KNIGHT

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen