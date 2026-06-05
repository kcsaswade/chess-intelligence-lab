from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_freer_side_scores_better_on_mobility() -> None:
    freer = parse_fen("4k3/8/8/8/8/8/4K3/7Q w - - 0 1")
    cramped = parse_fen("4k3/8/8/8/8/8/4K3/8 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=100, king_safety=0, pawn_structure=0, center_control=0, piece_activity=0)

    assert evaluate(freer, weights).mobility > evaluate(cramped, weights).mobility