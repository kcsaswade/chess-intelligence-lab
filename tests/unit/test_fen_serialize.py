from chesslab.engine.position import Position
from chesslab.io.fen import parse_fen, to_fen


def test_round_trip_start_position() -> None:
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert to_fen(parse_fen(fen)) == fen


def test_round_trip_empty_board() -> None:
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    assert to_fen(parse_fen(fen)) == fen


def test_position_method_round_trip() -> None:
    fen = "8/8/8/3pP3/8/8/8/8 w - d6 0 2"
    pos = Position.from_fen(fen)
    assert pos.to_fen() == fen


def test_serialize_parse_serialize() -> None:
    fen = "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 5 21"
    once = to_fen(parse_fen(fen))
    twice = to_fen(parse_fen(once))
    assert once == fen
    assert twice == fen