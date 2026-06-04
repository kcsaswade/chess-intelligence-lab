from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType


def test_move_equality() -> None:
    a = Move(from_sq=12, to_sq=28)
    b = Move(from_sq=12, to_sq=28)
    assert a == b


def test_move_promotion_field() -> None:
    move = Move(from_sq=52, to_sq=60, promotion=PieceType.QUEEN)
    assert move.promotion is PieceType.QUEEN


def test_move_capture_flag() -> None:
    move = Move(from_sq=10, to_sq=17, is_capture=True)
    assert move.is_capture is True