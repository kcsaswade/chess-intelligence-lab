from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType
from chesslab.io.fen import parse_fen


def test_castling_make_unmake_restores_fen() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    fen_before = position.to_fen()

    move = Move(from_sq=coord_to_index("e1"), to_sq=coord_to_index("g1"), is_castling=True)
    undo = make_move(position, move)

    assert position.piece_at(coord_to_index("g1")) is not None
    assert position.piece_at(coord_to_index("g1")).kind is PieceType.KING
    assert position.piece_at(coord_to_index("f1")) is not None
    assert position.piece_at(coord_to_index("f1")).kind is PieceType.ROOK

    unmake_move(position, move, undo)
    assert position.to_fen() == fen_before