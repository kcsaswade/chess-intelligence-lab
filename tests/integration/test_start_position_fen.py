from chesslab.engine.position import Position
from chesslab.engine.startpos import STARTPOS_FEN


def test_start_position_round_trips_exactly() -> None:
    position = Position.from_fen(STARTPOS_FEN)
    assert position.to_fen() == STARTPOS_FEN