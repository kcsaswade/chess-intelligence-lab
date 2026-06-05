from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_developed_minor_pieces_improve_activity() -> None:
    active = parse_fen("4k3/8/8/8/3N4/2B5/8/4K3 w - - 0 1")
    passive = parse_fen("4k3/8/8/8/8/8/8/2B1KN2 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=0, king_safety=0, pawn_structure=0, center_control=0, piece_activity=100)

    assert evaluate(active, weights).piece_activity > evaluate(passive, weights).piece_activity