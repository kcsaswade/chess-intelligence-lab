from chesslab.engine.eval.evaluator import evaluate
from chesslab.io.fen import parse_fen


def test_color_swapped_position_inverts_material() -> None:
    white_adv = parse_fen("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    black_adv = parse_fen("3qk3/8/8/8/8/8/8/4K3 w - - 0 1")

    assert evaluate(white_adv).material == -evaluate(black_adv).material