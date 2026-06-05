from chesslab.engine.eval.evaluator import evaluate_position
from chesslab.io.fen import parse_fen


def test_extra_white_queen_is_positive() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    result = evaluate_position(position)
    assert result.total > 0
    assert result.material > 0


def test_mirrored_material_inverts_sign() -> None:
    white_better = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    black_better = parse_fen("4kq2/8/8/8/8/8/8/4K3 w - - 0 1")
    assert evaluate_position(white_better).total == -evaluate_position(black_better).total