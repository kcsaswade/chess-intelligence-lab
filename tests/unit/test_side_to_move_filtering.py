from chesslab.engine.board import index_to_coord
from chesslab.engine.move_generation.generator import generate_pseudolegal_moves
from chesslab.io.fen import parse_fen


def test_only_side_to_move_generates_moves() -> None:
    position = parse_fen("8/8/8/3N4/8/8/4p3/8 b - - 0 1")
    moves = generate_pseudolegal_moves(position)
    destinations = {index_to_coord(move.to_sq) for move in moves}
    assert "e1" in destinations or "e3" in destinations or "e4" in destinations
    assert "b4" not in destinations