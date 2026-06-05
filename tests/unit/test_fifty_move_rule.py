from chesslab.engine.game_status import is_draw_by_fifty_move_rule
from chesslab.io.fen import parse_fen


def test_fifty_move_rule_detected_at_threshold() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 100 1")
    assert is_draw_by_fifty_move_rule(position)


def test_fifty_move_rule_not_detected_below_threshold() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 99 1")
    assert not is_draw_by_fifty_move_rule(position)