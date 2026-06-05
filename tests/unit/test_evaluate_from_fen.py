from chesslab.engine.eval.evaluator import evaluate
from chesslab.io.fen import parse_fen


def test_evaluate_from_fen_returns_structured_result() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    result = evaluate(position)

    assert isinstance(result.total, int)
    assert isinstance(result.material, int)
    assert isinstance(result.mobility, int)
    assert isinstance(result.king_safety, int)
    assert isinstance(result.pawn_structure, int)
    assert isinstance(result.center_control, int)
    assert isinstance(result.piece_activity, int)