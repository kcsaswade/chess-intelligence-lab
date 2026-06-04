from chesslab.engine.board import coord_to_index
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_make_unmake_king_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("e5"))

    undo = make_move(position, move)
    assert position.piece_at(coord_to_index("e5")) is not None
    assert position.piece_at(coord_to_index("e4")) is None

    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_make_unmake_knight_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/3N4/8/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("d5"), coord_to_index("f4"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_make_unmake_rook_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/8/4R3/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("e7"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_make_unmake_bishop_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/8/3B4/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("d4"), coord_to_index("g7"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_make_unmake_queen_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/8/4Q3/8/8/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e4"), coord_to_index("b7"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen


def test_make_unmake_pawn_quiet_move_roundtrip() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    original_fen = position.to_fen()
    move = Move(coord_to_index("e2"), coord_to_index("e3"))

    undo = make_move(position, move)
    unmake_move(position, move, undo)
    assert position.to_fen() == original_fen