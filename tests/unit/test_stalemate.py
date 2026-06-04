from chesslab.engine.attacks import is_in_check
from chesslab.engine.game_status import is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_basic_stalemate_1() -> None:
    position = parse_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert is_stalemate(position)


def test_basic_stalemate_2() -> None:
    position = parse_fen("k7/2Q5/1K6/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert is_stalemate(position)


def test_basic_stalemate_3() -> None:
    position = parse_fen("7k/5Q2/7K/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(position, Color.BLACK)
    assert len(generate_legal_moves(position)) == 0
    assert is_stalemate(position)