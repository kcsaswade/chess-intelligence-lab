from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.knight_moves import generate_knight_moves
from chesslab.io.fen import parse_fen


def _coords(moves: list) -> set[str]:
    return {index_to_coord(move.to_sq) for move in moves}


def test_knight_center_moves() -> None:
    position = parse_fen("8/8/8/3N4/8/8/8/8 w - - 0 1")
    moves = generate_knight_moves(position, coord_to_index("d5"))
    assert _coords(moves) == {"b4", "b6", "c3", "c7", "e3", "e7", "f4", "f6"}


def test_knight_corner_moves() -> None:
    position = parse_fen("8/8/8/8/8/8/8/N7 w - - 0 1")
    moves = generate_knight_moves(position, coord_to_index("a1"))
    assert _coords(moves) == {"b3", "c2"}


def test_knight_own_piece_blocks_destination() -> None:
    position = parse_fen("8/8/8/3N4/8/2P5/8/8 w - - 0 1")
    moves = generate_knight_moves(position, coord_to_index("d5"))
    assert "c3" not in _coords(moves)


def test_knight_enemy_piece_is_capture() -> None:
    position = parse_fen("8/8/8/3N4/8/2p5/8/8 w - - 0 1")
    moves = generate_knight_moves(position, coord_to_index("d5"))
    capture_squares = {index_to_coord(move.to_sq) for move in moves if move.is_capture}
    assert "c3" in capture_squares