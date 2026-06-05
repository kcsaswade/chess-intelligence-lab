from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_weight_change_scales_target_component() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")

    low = evaluate(
        position,
        EvaluationWeights(material=50, mobility=0, king_safety=0, pawn_structure=0, center_control=0, piece_activity=0),
    )
    high = evaluate(
        position,
        EvaluationWeights(material=200, mobility=0, king_safety=0, pawn_structure=0, center_control=0, piece_activity=0),
    )

    assert high.material > low.material
    assert high.total > low.total