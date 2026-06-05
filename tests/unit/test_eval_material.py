from chesslab.engine.eval.evaluator import evaluate
from chesslab.io.fen import parse_fen


def test_extra_queen_is_positive_for_white() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    result = evaluate(position)
    assert result.material > 0
    assert result.total > 0


def test_extra_rook_is_positive_for_white() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KR2 w - - 0 1")
    result = evaluate(position)
    assert result.material > 0


def test_material_mirror_inverts_sign() -> None:
    white_better = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    black_better = parse_fen("4kq2/8/8/8/8/8/8/4K3 w - - 0 1")
    assert evaluate(white_better).material == -evaluate(black_better).material