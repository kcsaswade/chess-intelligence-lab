from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_no_castling_while_in_check() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4r3/R3K2R w KQ - 0 1")
    moves = generate_legal_moves(position)
    assert not any(move.is_castling for move in moves)


def test_no_castling_through_attacked_square() -> None:
    position = parse_fen("4k3/8/8/8/2b5/8/8/R3K2R w KQ - 0 1")
    moves = generate_legal_moves(position)
    assert not any(move.is_castling and move.to_sq == 6 for move in moves)


def test_no_castling_into_attacked_square() -> None:
    position = parse_fen("4k3/8/8/8/8/8/6r1/R3K2R w KQ - 0 1")
    moves = generate_legal_moves(position)
    assert not any(move.is_castling and move.to_sq == 6 for move in moves)


def test_no_castling_without_rights() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/R3K2R w - - 0 1")
    moves = generate_legal_moves(position)
    assert not any(move.is_castling for move in moves)