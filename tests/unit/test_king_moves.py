from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.king_moves import generate_king_moves
from chesslab.io.fen import parse_fen


def _coords(moves: list) -> set[str]:
    return {index_to_coord(move.to_sq) for move in moves}


def test_king_center_moves() -> None:
    position = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    moves = generate_king_moves(position, coord_to_index("e4"))
    assert _coords(moves) == {"d3", "e3", "f3", "d4", "f4", "d5", "e5", "f5"}


def test_king_corner_moves() -> None:
    position = parse_fen("8/8/8/8/8/8/8/K7 w - - 0 1")
    moves = generate_king_moves(position, coord_to_index("a1"))
    assert _coords(moves) == {"a2", "b1", "b2"}


def test_king_own_piece_blocks_destination() -> None:
    position = parse_fen("8/8/8/8/4K3/4P3/8/8 w - - 0 1")
    moves = generate_king_moves(position, coord_to_index("e4"))
    assert "e3" not in _coords(moves)


def test_king_enemy_piece_is_capture() -> None:
    position = parse_fen("8/8/8/8/4K3/3p4/8/8 w - - 0 1")
    moves = generate_king_moves(position, coord_to_index("e4"))
    capture_squares = {index_to_coord(move.to_sq) for move in moves if move.is_capture}
    assert "d3" in capture_squares