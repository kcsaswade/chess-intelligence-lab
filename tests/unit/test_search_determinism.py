from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_search_is_deterministic() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    config = SearchConfig(depth=3, use_alpha_beta=True)

    first = search_position(position, config)
    second = search_position(position, config)

    assert first.best_move == second.best_move
    assert first.score == second.score
    assert first.stats.principal_variation == second.stats.principal_variation