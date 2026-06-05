from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_search_stats_are_populated() -> None:
    position = parse_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    result = search_position(position, SearchConfig(depth=2))
    assert result.stats.nodes > 0
    assert result.stats.cutoffs >= 0
    assert result.stats.depth_reached <= 2
    assert result.stats.time_ms >= 0.0