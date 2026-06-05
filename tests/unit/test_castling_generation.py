from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_white_both_castles_generated_when_clear() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    moves = generate_legal_moves(position)
    pairs = {(move.from_sq, move.to_sq, move.is_castling) for move in moves}
    assert (coord_to_index("e1"), coord_to_index("g1"), True) in pairs
    assert (coord_to_index("e1"), coord_to_index("c1"), True) in pairs


def test_black_both_castles_generated_when_clear() -> None:
    position = parse_fen("r3k2r/8/8/8/8/8/8/4K3 b kq - 0 1")
    moves = generate_legal_moves(position)
    pairs = {(move.from_sq, move.to_sq, move.is_castling) for move in moves}
    assert (coord_to_index("e8"), coord_to_index("g8"), True) in pairs
    assert (coord_to_index("e8"), coord_to_index("c8"), True) in pairs


def test_no_castling_when_path_blocked() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/R3KB1R w KQ - 0 1")
    moves = generate_legal_moves(position)

    assert not any(move.is_castling and move.to_sq == coord_to_index("g1") for move in moves)
    assert any(move.is_castling and move.to_sq == coord_to_index("c1") for move in moves)