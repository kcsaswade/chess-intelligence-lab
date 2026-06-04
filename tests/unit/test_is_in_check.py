from chesslab.engine.attacks import is_in_check
from chesslab.engine.piece import Color
from chesslab.io.fen import parse_fen


def test_not_in_check() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert not is_in_check(position, Color.WHITE)
    assert not is_in_check(position, Color.BLACK)


def test_in_rook_check() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4r3/4K3 w - - 0 1")
    assert is_in_check(position, Color.WHITE)


def test_in_bishop_check() -> None:
    position = parse_fen("4k3/8/8/8/8/2b5/8/4K3 w - - 0 1")
    assert is_in_check(position, Color.WHITE)


def test_in_knight_check() -> None:
    position = parse_fen("4k3/8/8/8/8/3n4/8/4K3 w - - 0 1")
    assert is_in_check(position, Color.WHITE)


def test_in_pawn_check() -> None:
    position = parse_fen("4k3/8/8/8/8/8/3p4/4K3 w - - 0 1")
    assert is_in_check(position, Color.WHITE)