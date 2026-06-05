from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_search_accepts_weight_overrides() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    weights = EvaluationWeights(
        material=100,
        mobility=25,
        king_safety=30,
        pawn_structure=15,
        center_control=20,
        piece_activity=18,
    )
    result = search_position(position, SearchConfig(depth=2, evaluation_weights=weights))
    assert result.best_move is not None
    assert result.stats.nodes > 0