from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_center_occupation_and_control_help_score() -> None:
    centered = parse_fen("4k3/8/8/3P4/4P3/8/8/4K3 w - - 0 1")
    edge = parse_fen("4k3/8/8/P7/7P/8/8/4K3 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=0, king_safety=0, pawn_structure=0, center_control=100, piece_activity=0)

    assert evaluate(centered, weights).center_control > evaluate(edge, weights).center_control