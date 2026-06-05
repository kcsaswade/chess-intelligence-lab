from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_pawn_shield_improves_king_safety() -> None:
    safe = parse_fen("4k3/8/8/8/8/8/5PPP/6K1 w - - 0 1")
    exposed = parse_fen("4k3/8/8/8/8/8/8/6K1 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=0, king_safety=100, pawn_structure=0, center_control=0, piece_activity=0)

    assert evaluate(safe, weights).king_safety > evaluate(exposed, weights).king_safety