from chesslab.engine.attacks import is_in_check
from chesslab.engine.game_status import is_checkmate
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_simple_rook_mate() -> None:
    position = parse_fen("7k/6R1/6K1/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert not is_checkmate(position)


def test_simple_queen_mate() -> None:
    position = parse_fen("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")
    assert is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert is_checkmate(position)


def test_corner_mate_pattern() -> None:
    position = parse_fen("k7/1R6/2K5/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert not is_checkmate(position)