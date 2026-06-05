from chesslab.engine.board import coord_to_index
from chesslab.engine.game_status import is_draw_by_repetition
from chesslab.engine.history import PositionHistory
from chesslab.engine.make_unmake import make_move
from chesslab.engine.move import Move
from chesslab.io.fen import parse_fen


def test_threefold_repetition_detected() -> None:
    position = parse_fen("4k3/8/8/8/8/8/6N1/4K2n w - - 0 1")
    history = PositionHistory.from_position(position)

    cycle = [
        Move(coord_to_index("g2"), coord_to_index("f4")),
        Move(coord_to_index("h1"), coord_to_index("f2")),
        Move(coord_to_index("f4"), coord_to_index("g2")),
        Move(coord_to_index("f2"), coord_to_index("h1")),
    ]

    for _ in range(2):
        for move in cycle:
            make_move(position, move)
            history.record(position)

    assert is_draw_by_repetition(position, history)