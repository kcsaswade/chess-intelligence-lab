from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.stats import SearchStats
from chesslab.io.serializers import (
    evaluation_result_to_dict,
    search_config_to_dict,
    search_stats_to_dict,
)


def test_serializers_are_stable_and_deterministic() -> None:
    evaluation = EvaluationResult(10, 1, 2, 3, 4, 5, 6)
    stats = SearchStats(100, 10, 3, 5.5, [])
    config = SearchConfig(depth=3)

    assert evaluation_result_to_dict(evaluation) == {
        "total": 10,
        "material": 1,
        "mobility": 2,
        "king_safety": 3,
        "pawn_structure": 4,
        "center_control": 5,
        "piece_activity": 6,
    }
    assert search_stats_to_dict(stats)["nodes"] == 100
    assert search_config_to_dict(config)["depth"] == 3