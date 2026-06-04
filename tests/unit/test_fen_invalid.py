import pytest

from chesslab.errors import FenError
from chesslab.io.fen import parse_fen


def test_too_few_fields() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - 0")


def test_too_many_fields() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - 0 1 extra")


def test_invalid_side_to_move() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 x - - 0 1")


def test_invalid_castling_field() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w KX - 0 1")


def test_invalid_en_passant_square() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - z9 0 1")


def test_invalid_en_passant_rank() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - e4 0 1")


def test_non_integer_halfmove() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - x 1")


def test_non_integer_fullmove() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - 0 y")


def test_negative_halfmove() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - -1 1")


def test_non_positive_fullmove() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w - - 0 0")


def test_bad_rank_width() -> None:
    with pytest.raises(FenError):
        parse_fen("9/8/8/8/8/8/8/8 w - - 0 1")


def test_too_few_ranks() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8 w - - 0 1")


def test_too_many_ranks() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8/8 w - - 0 1")


def test_duplicate_castling_rights() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w KK - 0 1")


def test_non_canonical_castling_order() -> None:
    with pytest.raises(FenError):
        parse_fen("8/8/8/8/8/8/8/8 w qK - 0 1")