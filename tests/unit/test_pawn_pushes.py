from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.pawn_moves import generate_pawn_moves
from chesslab.io.fen import parse_fen


def _coords(moves: list) -> set[str]:
    return {index_to_coord(move.to_sq) for move in moves}


def test_white_pawn_single_push() -> None:
    position = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e2"))
    assert "e3" in _coords(moves)


def test_black_pawn_single_push() -> None:
    position = parse_fen("8/3p4/8/8/8/8/8/8 b - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("d7"))
    assert "d6" in _coords(moves)


def test_pawn_blocked_forward() -> None:
    position = parse_fen("8/8/8/8/8/4p3/4P3/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e2"))
    assert "e3" not in _coords(moves)