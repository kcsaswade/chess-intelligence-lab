from chesslab.engine.eval.evaluator import evaluate
from chesslab.io.fen import parse_fen


def test_evaluation_is_deterministic() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    first = evaluate(position)
    second = evaluate(position)
    assert first == second