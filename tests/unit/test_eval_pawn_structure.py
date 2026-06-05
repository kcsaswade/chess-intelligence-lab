from chesslab.engine.eval.evaluator import evaluate
from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.io.fen import parse_fen


def test_doubled_pawns_are_penalized() -> None:
    healthy = parse_fen("4k3/8/8/8/8/8/4P3/4K3 w - - 0 1")
    doubled = parse_fen("4k3/8/8/8/8/4P3/4P3/4K3 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=0, king_safety=0, pawn_structure=100, center_control=0, piece_activity=0)

    assert evaluate(healthy, weights).pawn_structure > evaluate(doubled, weights).pawn_structure


def test_isolated_pawns_are_penalized() -> None:
    connected = parse_fen("4k3/8/8/8/8/8/3PP3/4K3 w - - 0 1")
    isolated = parse_fen("4k3/8/8/8/8/8/3P4/4K1P1 w - - 0 1")
    weights = EvaluationWeights(material=0, mobility=0, king_safety=0, pawn_structure=100, center_control=0, piece_activity=0)

    assert evaluate(connected, weights).pawn_structure > evaluate(isolated, weights).pawn_structure