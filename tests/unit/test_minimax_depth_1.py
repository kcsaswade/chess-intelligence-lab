from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_depth_1_prefers_free_queen_capture() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4q3/3QK3 w - - 0 1")
    result = search_position(position, SearchConfig(depth=1))
    assert result.best_move is not None
    assert result.best_move.is_capture is True
    assert result.score > 0