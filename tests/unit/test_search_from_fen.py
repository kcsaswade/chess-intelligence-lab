from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_search_from_fen_returns_structured_result() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    result = search_position(position, SearchConfig(depth=2))
    assert result.best_move is not None
    assert isinstance(result.score, int)
    assert result.stats.nodes > 0
    assert result.stats.principal_variation