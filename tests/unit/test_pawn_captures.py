from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.pawn_moves import generate_pawn_moves
from chesslab.io.fen import parse_fen


def test_white_pawn_captures() -> None:
    position = parse_fen("8/8/8/2p1p3/3P4/8/8/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("d4"))
    capture_squares = {index_to_coord(move.to_sq) for move in moves if move.is_capture}
    assert capture_squares == {"c5", "e5"}


def test_black_pawn_captures() -> None:
    position = parse_fen("8/8/8/8/8/3p4/2P1P3/8 b - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("d3"))
    capture_squares = {index_to_coord(move.to_sq) for move in moves if move.is_capture}
    assert capture_squares == {"c2", "e2"}