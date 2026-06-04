from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.pawn_moves import generate_pawn_moves
from chesslab.io.fen import parse_fen


def test_white_double_push_available() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e2"))
    coords = {index_to_coord(move.to_sq) for move in moves}
    assert "e4" in coords
    assert any(move.is_double_pawn_push for move in moves)


def test_black_double_push_available() -> None:
    position = parse_fen("8/3p4/8/8/8/8/8/8 b - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("d7"))
    coords = {index_to_coord(move.to_sq) for move in moves}
    assert "d5" in coords
    assert any(move.is_double_pawn_push for move in moves)


def test_double_push_requires_clear_intermediate_and_destination() -> None:
    position = parse_fen("8/8/8/8/4p3/8/4P3/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e2"))
    coords = {index_to_coord(move.to_sq) for move in moves}
    assert "e4" not in coords